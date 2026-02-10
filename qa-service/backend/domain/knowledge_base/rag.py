# encoding: utf-8
"""
RAG引擎，实现检索增强生成功能。
"""
from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional

from infrastructure.embedding.service import EmbeddingService
from infrastructure.llm.service import LLMService
from shared.logger import log
from shared.utils.text_splitter import TextSplitter
from infrastructure.vector_store.chroma import VectorStore


class RAGEngine:
    """RAG引擎，实现检索增强生成。"""

    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        embedding_service: Optional[EmbeddingService] = None,
        llm_service: Optional[LLMService] = None,
        top_k: Optional[int] = None,
        similarity_threshold: Optional[float] = None,
        max_context_length: Optional[int] = None,
    ):
        """
        初始化RAG引擎。

        Args:
            vector_store: 向量存储服务，如果不提供则自动创建
            embedding_service: Embedding服务，如果不提供则自动创建
            llm_service: LLM服务，如果不提供则自动创建
            top_k: 检索返回的文档数量，如果不提供则使用配置中的默认值
            similarity_threshold: 相似度阈值，如果不提供则使用配置中的默认值
            max_context_length: 上下文最大长度，如果不提供则使用配置中的默认值
        """
        # 延迟初始化，只有在实际使用时才创建（避免导入时检查依赖）
        self._vector_store = vector_store
        self._embedding_service = embedding_service
        self._llm_service = llm_service
        # 增加chunk_size以提升上下文完整性，chunk_overlap保持合理重叠
        self.text_splitter = TextSplitter(chunk_size=800, chunk_overlap=100)

        # 从环境变量或配置读取参数
        self.top_k = top_k or int(os.getenv("RAG_TOP_K", "15"))  # 增加检索数量，提升召回率
        self.similarity_threshold = similarity_threshold or float(
            os.getenv("RAG_SIMILARITY_THRESHOLD", "0.45")  # 适当降低阈值，允许更多相关文档
        )
        self.max_context_length = max_context_length or int(
            os.getenv("RAG_MAX_CONTEXT_LENGTH", "5000")  # 增加上下文长度，提供更多信息
        )

    @property
    def vector_store(self) -> VectorStore:
        """获取向量存储（延迟初始化）。"""
        if self._vector_store is None:
            self._vector_store = VectorStore()
        return self._vector_store

    @property
    def embedding_service(self) -> EmbeddingService:
        """获取Embedding服务（延迟初始化）。"""
        if self._embedding_service is None:
            self._embedding_service = EmbeddingService()
        return self._embedding_service

    @property
    def llm_service(self) -> LLMService:
        """获取LLM服务（延迟初始化）。"""
        if self._llm_service is None:
            self._llm_service = LLMService()
        return self._llm_service

    def index_documents(
        self,
        documents: List[Dict[str, Any]],
        batch_size: int = 10,
    ) -> int:
        """
        索引文档到向量存储。

        Args:
            documents: 文档列表，每个文档包含：
                - content: 文档内容
                - metadata: 文档元数据（包含title、url等）
                - id: 文档ID（可选）
            batch_size: 批量处理大小

        Returns:
            成功索引的文档数量
        """
        indexed_count = 0

        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]

            texts = []
            metadatas = []
            ids = []

            for doc in batch:
                content = doc.get("content", "")
                if not content or not content.strip():
                    continue

                # 分割文本
                chunks = self.text_splitter.split_text(content)

                # 为每个块创建向量（过滤掉太短的chunk）
                MIN_CHUNK_LENGTH = 30  # 最小chunk长度：30字符（放宽限制）
                valid_chunks = []
                for chunk_idx, chunk in enumerate(chunks):
                    # 过滤掉太短的chunk（这些chunk通常是不完整的，会导致错误的相似度匹配）
                    if len(chunk.strip()) >= MIN_CHUNK_LENGTH:
                        valid_chunks.append((chunk_idx, chunk))
                    else:
                        log.debug(f"跳过太短的chunk（{len(chunk)}字符）: {chunk[:30]}...")

                # 为有效的chunk创建向量
                for chunk_idx, chunk in valid_chunks:
                    doc_id = doc.get("id", f"doc_{i}_{chunk_idx}")
                    chunk_id = f"{doc_id}_chunk_{chunk_idx}"

                    texts.append(chunk)
                    metadatas.append({
                        **doc.get("metadata", {}),
                        "chunk_index": chunk_idx,
                        "total_chunks": len(chunks),
                    })
                    ids.append(chunk_id)

            if texts:
                # 批量向量化
                vectors = self.embedding_service.embed_batch(texts)

                # 添加到向量存储（使用预计算的向量）
                self.vector_store.add_documents(
                    texts=texts,
                    metadatas=metadatas,
                    ids=ids,
                    embeddings=vectors,
                )

                indexed_count += len(texts)

        log.info(f"成功索引 {indexed_count} 个文档块")
        return indexed_count

    def search(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        搜索相关文档。

        Args:
            query: 查询文本
            top_k: 返回结果数量，如果不提供则使用默认值

        Returns:
            搜索结果列表，每个结果包含文档、元数据和相似度
        """
        if not query or not query.strip():
            return []

        top_k = top_k or self.top_k

        # 简化查询扩展：只生成1-2个最相关的查询变体
        expanded_queries = self._expand_query(query)
        log.debug(f"查询扩展: 原始查询='{query}', 扩展查询={expanded_queries}")
        
        # 合并所有查询的结果
        all_results = []
        seen_chunk_ids = set()  # 用于去重：避免重复的chunk
        
        for expanded_query in expanded_queries:
            # 将查询向量化
            query_vector = self.embedding_service.embed_text(expanded_query)

            # 在向量存储中搜索（搜索更多结果，后续会过滤）
            results = self.vector_store.search(
                query_vectors=[query_vector],
                n_results=top_k * 2,
            )
            
            # 添加结果（去重）
            for result in results:
                chunk_id = result.get("id", "")
                if chunk_id and chunk_id not in seen_chunk_ids:
                    seen_chunk_ids.add(chunk_id)
                    all_results.append(result)
        
        # 如果没有结果，使用原始查询
        if not all_results:
            query_vector = self.embedding_service.embed_text(query)
            results = self.vector_store.search(
                query_vectors=[query_vector],
                n_results=top_k * 2,
            )
            all_results = results
        
        # 按相似度排序
        all_results.sort(key=lambda x: x.get("similarity", 0), reverse=True)

        # 过滤掉太短的chunk
        MIN_CHUNK_LENGTH = 30
        filtered_results = []
        for result in all_results:
            content = result.get("document", "")
            if len(content.strip()) >= MIN_CHUNK_LENGTH:
                filtered_results.append(result)
            else:
                log.debug(f"过滤掉太短的chunk（{len(content)}字符）: {content[:30]}...")
        
        # 限制返回数量
        filtered_results = filtered_results[:top_k]

        # 过滤低相似度结果（动态调整阈值）
        final_results = []
        dynamic_threshold = self.similarity_threshold
        if filtered_results:
            max_sim = max([r.get("similarity", 0) for r in filtered_results])
            # 如果最高相似度在0.4-0.5之间，适当降低阈值
            if max_sim < 0.5 and max_sim >= 0.4:
                dynamic_threshold = 0.4
                log.debug(f"动态调整相似度阈值: {self.similarity_threshold} -> {dynamic_threshold} (最高相似度: {max_sim:.3f})")
        
        for result in filtered_results:
            similarity = result.get("similarity", 0)
            if similarity >= dynamic_threshold:
                final_results.append(result)
            else:
                log.debug(f"文档相似度 {similarity:.3f} 低于阈值 {dynamic_threshold}，已过滤")
        
        log.info(f"向量搜索返回 {len(all_results)} 个结果，过滤后剩余 {len(final_results)} 个（阈值: {dynamic_threshold}）")
        
        return final_results
    
    def _expand_query(self, query: str) -> List[str]:
        """
        扩展查询，生成少量相关的查询变体以提升检索效果。
        
        Args:
            query: 原始查询
            
        Returns:
            查询变体列表（包含原始查询，最多3个）
        """
        queries = [query]  # 始终包含原始查询
        
        # 简化的查询扩展策略：只生成最相关的1-2个变体
        question_words = {"如何", "怎么", "怎样", "什么", "为什么"}
        
        # 对于"如何/怎么/怎样"类问题，提取核心关键词
        if any(keyword in query for keyword in ["如何", "怎么", "怎样"]):
            # 移除疑问词，保留核心概念
            core_query = query
            for qw in question_words:
                core_query = core_query.replace(qw, " ").strip()
            # 清理多余空格
            core_query = " ".join(core_query.split())
            if core_query and core_query != query and len(core_query) > 2:
                queries.append(core_query)
        
        # 如果查询包含"是什么"、"什么是"，生成一个变体
        elif "是什么" in query or "什么是" in query:
            core_query = query.replace("是什么", "").replace("什么是", "").strip()
            if core_query and len(core_query) > 2:
                queries.append(core_query)
        
        # 去重并限制变体数量（最多3个，包括原始查询）
        seen = set()
        unique_queries = []
        for q in queries:
            q_clean = q.strip()
            if q_clean and q_clean not in seen:
                seen.add(q_clean)
                unique_queries.append(q_clean)
                if len(unique_queries) >= 3:
                    break
        
        return unique_queries

    def generate_answer(
        self,
        question: str,
        context_documents: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        生成答案。

        Args:
            question: 用户问题
            context_documents: 上下文文档列表，如果不提供则自动检索

        Returns:
            答案字典，包含：
                - answer: 生成的答案
                - sources: 引用来源列表
                - context: 使用的上下文
        """
        # 如果没有提供上下文文档，则自动检索
        if context_documents is None:
            context_documents = self.search(question)

        # 构建上下文：按相似度排序，智能去重和截断
        sorted_docs = sorted(context_documents, key=lambda x: x.get("similarity", 0), reverse=True)
        
        context_parts = []
        sources = []
        seen_titles = {}  # 用于去重：key为title，value为最高相似度
        MAX_CHUNKS_PER_DOC = 2  # 每篇文章最多保留2个chunk

        for doc in sorted_docs:
            content = doc.get("document", "")
            metadata = doc.get("metadata", {})
            similarity = doc.get("similarity", 0)
            title = metadata.get("title", "未知标题")

            if not content or not content.strip():
                continue

            # 简化去重策略：同一篇文章最多保留2个最高相似度的chunk
            if title in seen_titles:
                existing_count, max_sim = seen_titles[title]
                # 如果已有chunk数量未达到上限，且当前chunk相似度较高，则添加
                if existing_count < MAX_CHUNKS_PER_DOC and similarity >= 0.5:
                    context_parts.append(content)
                    sources.append({
                        "title": title,
                        "url": metadata.get("url", ""),
                        "similarity": similarity,
                    })
                    seen_titles[title] = (existing_count + 1, max(max_sim, similarity))
                # 如果已有chunk但当前chunk相似度更高，替换相似度最低的
                elif similarity > max_sim:
                    # 找到该文档的第一个chunk并替换
                    for i, source in enumerate(sources):
                        if source["title"] == title:
                            context_parts[i] = content
                            sources[i] = {
                                "title": title,
                                "url": metadata.get("url", ""),
                                "similarity": similarity,
                            }
                            seen_titles[title] = (existing_count, similarity)
                            break
                continue
            
            # 新文章，添加到结果中
            seen_titles[title] = (1, similarity)
            context_parts.append(content)
            sources.append({
                "title": title,
                "url": metadata.get("url", ""),
                "similarity": similarity,
            })

        # 智能截断上下文：优先保留高相似度的chunk
        context = "\n\n".join(context_parts)
        if len(context) > self.max_context_length:
            # 按相似度排序，优先保留高相似度的chunk
            chunk_with_sim = list(zip(context_parts, [s["similarity"] for s in sources]))
            chunk_with_sim.sort(key=lambda x: x[1], reverse=True)
            
            truncated_parts = []
            total_length = 0
            for content, sim in chunk_with_sim:
                chunk_len = len(content) + 2  # 加上分隔符长度
                if total_length + chunk_len <= self.max_context_length:
                    truncated_parts.append(content)
                    total_length += chunk_len
                else:
                    # 如果还有空间，添加部分内容
                    remaining = self.max_context_length - total_length - 2
                    if remaining > 100:  # 至少保留100字符
                        truncated_parts.append(content[:remaining] + "...")
                    break
            
            # 重新组合上下文
            context = "\n\n".join(truncated_parts)

        # 计算相似度统计
        max_similarity = max([doc.get("similarity", 0) for doc in context_documents]) if context_documents else 0.0
        avg_similarity = sum([doc.get("similarity", 0) for doc in context_documents]) / len(context_documents) if context_documents else 0.0

        # 去重sources：同一文档只保留一次（使用最高相似度）
        unique_sources = {}
        for source in sources:
            title = source["title"]
            if title not in unique_sources or source["similarity"] > unique_sources[title]["similarity"]:
                unique_sources[title] = source
        
        # 转换为列表并按相似度排序
        final_sources = list(unique_sources.values())
        final_sources.sort(key=lambda x: x["similarity"], reverse=True)

        # 简化的标题相关性检查：检查标题是否包含问题的核心关键词
        document_titles = [source["title"] for source in final_sources[:5]]
        title_relevant = False
        if document_titles:
            import re
            # 提取问题的核心关键词（英文单词和2-4字中文词汇）
            english_words = re.findall(r'[a-zA-Z]+', question.lower())
            chinese_text = ''.join(re.findall(r'[\u4e00-\u9fa5]+', question))
            chinese_words = []
            for length in range(2, min(5, len(chinese_text) + 1)):
                for i in range(len(chinese_text) - length + 1):
                    chinese_words.append(chinese_text[i:i+length])
            
            # 移除停用词
            stop_words = {"如何", "怎么", "怎样", "什么", "为什么", "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这"}
            question_keywords = {kw for kw in (english_words + chinese_words) if kw not in stop_words and len(kw) > 1}
            
            # 检查标题是否包含关键词
            for title in document_titles:
                title_lower = title.lower()
                matched = sum(1 for kw in question_keywords if (kw.isascii() and kw in title_lower) or (not kw.isascii() and kw in title))
                if matched >= 2:  # 至少匹配2个关键词
                    title_relevant = True
                    log.info(f"✅ 文档标题相关: '{title}' 匹配到 {matched} 个关键词")
                    break
        
        log.debug(f"检索到的文档标题: {document_titles}, 相关性: {title_relevant}, 上下文长度: {len(context)} 字符")

        # 构建Prompt
        prompt = self._build_qa_prompt(question, context, max_similarity, avg_similarity, document_titles, title_relevant)

        # 生成答案
        try:
            answer = self.llm_service.generate(prompt)
        except Exception as e:
            log.error(f"生成答案失败: {e}")
            answer = "抱歉，生成答案时出现错误，请稍后重试。"

        answer_text = answer.strip()
        
        # 清理答案中的提示性文字（后处理）
        answer_text = self._clean_answer(answer_text)
        
        # 如果文档标题明显相关但AI判断不相关，简化处理：保留sources但记录警告
        not_relevant_keywords = [
            "没有找到直接相关的文档",
            "没有找到相关文档",
            "知识库中没有找到",
            "文档内容与问题不相关",
        ]
        
        is_not_relevant = any(keyword in answer_text for keyword in not_relevant_keywords)
        if is_not_relevant and title_relevant:
            log.warning(f"⚠️ AI判断文档不相关，但文档标题明显相关，保留sources")
        
        return {
            "answer": answer_text,
            "sources": final_sources,
            "context": context,
        }

    def _build_qa_prompt(self, question: str, context: str, max_similarity: float = 0.0, avg_similarity: float = 0.0, document_titles: Optional[List[str]] = None, title_relevant: bool = False) -> str:
        """
        构建问答Prompt（简化版，减少复杂的判断逻辑）。

        Args:
            question: 用户问题
            context: 上下文文档
            max_similarity: 最高相似度
            avg_similarity: 平均相似度
            document_titles: 文档标题列表
            title_relevant: 文档标题是否明显相关

        Returns:
            完整的Prompt
        """
        # 简化的相关性提示
        if title_relevant:
            relevance_hint = f"⚠️ 重要提示：检索到的文档标题（{', '.join(document_titles[:3]) if document_titles else '无'}）明显与问题相关，请基于文档内容回答问题。"
        elif max_similarity >= 0.6:
            relevance_hint = "文档与问题相关，请基于文档内容回答问题。"
        elif max_similarity >= 0.5:
            relevance_hint = "文档与问题部分相关，请基于文档内容回答，如果文档中没有直接答案，可以说明文档中相关的内容。"
        else:
            relevance_hint = "文档相关性较低，如果文档内容与问题不相关，请明确说明'知识库中没有找到直接相关的文档，建议使用网络搜索'。"

        return f"""你是一位专业的AI助手，需要基于提供的文档内容回答用户问题。

【核心原则】
1. **只能基于提供的文档内容回答，不能基于一般知识或经验回答**
2. **如果文档标题明显相关（已标注），必须认为相关并回答问题**
3. **如果文档不相关，明确说明不相关，不要给出任何建议**
4. **重要：只输出答案本身，不要输出任何提示性文字（如"根据提供的文档内容"、"基于文档内容回答"等）**

{relevance_hint}

【文档内容】
{context}

【用户问题】
{question}

【相似度信息】
最高相似度: {max_similarity:.3f}, 平均相似度: {avg_similarity:.3f}

【要求】
1. **理解问题**：准确理解用户问题的核心意图
2. **判断相关性**：
   - 如果文档标题明显相关（已标注），必须认为相关
   - 如果文档内容回答了问题，认为相关
   - 如果文档内容与问题不相关，明确说明不相关
3. **回答问题**：
   - 如果相关：**直接回答用户问题**，可以引用文档中的具体内容，但不要说明"根据文档内容"、"基于文档内容"等提示性文字
   - 如果不相关：明确说明"知识库中没有找到直接相关的文档。检索到的文档主要涉及[主题]，与您的问题不直接相关。建议使用网络搜索获取更准确的信息。"

【输出格式要求】
- **禁止输出**：任何提示性文字，如"根据提供的文档内容"、"基于文档内容回答"、"文档标题相关"等
- **只输出**：直接回答用户问题的内容，或说明不相关的信息
- **示例**：
  ❌ 错误："根据提供的文档内容，mac如何抓包的相关信息确实存在，因此基于文档内容回答..."
  ✅ 正确：直接给出mac抓包的方法和步骤

【答案】
"""

    def _clean_answer(self, answer: str) -> str:
        """
        清理答案中的提示性文字，确保只返回答案本身。
        
        Args:
            answer: 原始答案
            
        Returns:
            清理后的答案
        """
        if not answer:
            return answer
        
        cleaned = answer
        
        # 移除常见的提示性开头短语（精确匹配）
        prefix_patterns = [
            r"^根据提供的文档内容[，,，]?\s*",
            r"^基于文档内容[，,，]?\s*",
            r"^根据提供的文档内容[，,，]?\s*.*?相关信息确实存在[，,，]?\s*",
            r"^.*?相关信息确实存在[，,，]?\s*",
            r"^.*?文档标题.*?相关[，,，]?\s*",
            r"^因此[，,，]?\s*",
            r"^基于.*?回答.*?问题[：:]\s*",
            r"^根据.*?回答.*?问题[：:]\s*",
        ]
        
        for pattern in prefix_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
        
        # 移除句子中间的提示性短语
        mid_patterns = [
            r"根据提供的文档内容[，,，]?\s*",
            r"基于文档内容[，,，]?\s*",
            r"文档标题.*?相关[，,，]?\s*",
            r"相关信息确实存在[，,，]?\s*",
            r"因此[，,，]?\s*基于文档内容回答",
            r"因此[，,，]?\s*根据文档内容回答",
        ]
        
        for pattern in mid_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
        
        # 清理多余的空格和换行
        cleaned = re.sub(r"\s+", " ", cleaned)  # 多个空格合并为一个
        cleaned = cleaned.strip()
        
        # 如果清理后内容太短，返回原答案（避免过度清理）
        if len(cleaned) < len(answer) * 0.3:
            log.warning(f"清理后答案过短（原长度: {len(answer)}, 清理后: {len(cleaned)}），保留原答案")
            return answer
        
        return cleaned

    def qa(self, question: str) -> Dict[str, Any]:
        """
        完整的问答流程：检索 + 生成答案。

        Args:
            question: 用户问题

        Returns:
            答案字典，包含answer、sources、context、max_similarity、avg_similarity
        """
        log.info(f"处理问题: {question}")

        # 检索相关文档
        context_documents = self.search(question)
        log.info(f"检索到 {len(context_documents)} 个相关文档块")
        
        # 如果没有找到相关文档，直接返回
        if not context_documents:
            log.warning(f"未找到相关文档（相似度阈值: {self.similarity_threshold}），可能知识库中没有相关内容")
            return {
                "answer": f"抱歉，在知识库中没有找到与您的问题相关的文档（相似度阈值: {self.similarity_threshold:.1%}）。\n\n建议：\n1. 尝试使用不同的关键词重新提问\n2. 检查知识库中是否有相关文章\n3. 如果问题涉及特定工具或概念，可以尝试使用更通用的关键词",
                "sources": [],
                "context": "",
                "max_similarity": 0.0,
                "avg_similarity": 0.0,
            }

        # 计算平均相似度，用于判断文档相关性
        avg_similarity = sum([doc.get("similarity", 0) for doc in context_documents]) / len(context_documents)
        max_similarity = max([doc.get("similarity", 0) for doc in context_documents])
        log.info(f"文档相似度统计: 最高={max_similarity:.3f}, 平均={avg_similarity:.3f}")

        # 如果平均相似度太低，给出提示
        if avg_similarity < 0.6:
            log.warning(f"文档平均相似度较低({avg_similarity:.3f})，可能不够相关，建议用户使用网络搜索")
        
        # 记录检索到的文档标题，便于调试
        if context_documents:
            titles = [doc.get("metadata", {}).get("title", "未知") for doc in context_documents[:5]]
            log.info(f"检索到的文档标题（前5个）: {titles}")

        # 生成答案
        result = self.generate_answer(question, context_documents)
        
        # 在结果中添加相似度信息
        result["max_similarity"] = max_similarity
        result["avg_similarity"] = avg_similarity

        return result

