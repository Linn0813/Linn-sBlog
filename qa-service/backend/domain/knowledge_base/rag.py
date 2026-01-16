# encoding: utf-8
"""
RAG引擎，实现检索增强生成功能。
"""
from __future__ import annotations

import os
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
        self.text_splitter = TextSplitter(chunk_size=500, chunk_overlap=50)

        # 从环境变量或配置读取参数
        self.top_k = top_k or int(os.getenv("RAG_TOP_K", "10"))  # 增加检索数量
        self.similarity_threshold = similarity_threshold or float(
            os.getenv("RAG_SIMILARITY_THRESHOLD", "0.5")  # 降低阈值，允许更多相关文档
        )
        self.max_context_length = max_context_length or int(
            os.getenv("RAG_MAX_CONTEXT_LENGTH", "4000")  # 增加上下文长度
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

        # 将查询向量化
        query_vector = self.embedding_service.embed_text(query)

        # 在向量存储中搜索
        results = self.vector_store.search(
            query_vectors=[query_vector],
            n_results=top_k * 2,  # 搜索更多结果，用于过滤短chunk
        )

        # 过滤掉太短的chunk（这些chunk通常是不完整的，会导致错误的相似度匹配）
        # 最小chunk长度：30字符（中文约15个字），放宽限制以避免过度过滤
        MIN_CHUNK_LENGTH = 30
        filtered_results = []
        for result in results:
            content = result.get("document", "")
            # 只保留长度足够的chunk
            if len(content.strip()) >= MIN_CHUNK_LENGTH:
                filtered_results.append(result)
            else:
                log.debug(f"过滤掉太短的chunk（{len(content)}字符）: {content[:30]}...")

        # 按相似度排序
        filtered_results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        
        # 限制返回数量
        filtered_results = filtered_results[:top_k]

        # 过滤低相似度结果
        final_results = []
        for result in filtered_results:
            similarity = result.get("similarity", 0)
            if similarity >= self.similarity_threshold:
                final_results.append(result)
            else:
                log.debug(f"文档相似度 {similarity:.3f} 低于阈值 {self.similarity_threshold}，已过滤")
        
        log.info(f"向量搜索返回 {len(results)} 个结果，过滤短chunk后剩余 {len(filtered_results)} 个，最终返回 {len(final_results)} 个（阈值: {self.similarity_threshold}）")
        
        return final_results

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

        # 构建上下文（去重：同一篇文章的不同chunk只保留相似度最高的）
        # 先按相似度排序，然后去重，确保保留相似度最高的chunk
        sorted_docs = sorted(context_documents, key=lambda x: x.get("similarity", 0), reverse=True)
        
        context_parts = []
        sources = []
        seen_titles = {}  # 用于去重：key为title，value为(index, similarity)

        for doc in sorted_docs:
            content = doc.get("document", "")
            metadata = doc.get("metadata", {})
            similarity = doc.get("similarity", 0)
            title = metadata.get("title", "未知标题")

            if not content or not content.strip():
                continue

            # 去重：如果已经见过这篇文章，只保留相似度更高的chunk
            if title in seen_titles:
                existing_idx, existing_sim = seen_titles[title]
                # 如果当前chunk相似度更高，替换
                if similarity > existing_sim:
                    context_parts[existing_idx] = content
                    sources[existing_idx] = {
                        "title": title,
                        "url": metadata.get("url", ""),
                        "similarity": similarity,
                    }
                    seen_titles[title] = (existing_idx, similarity)
                # 否则跳过（保留已有的更高相似度的chunk）
                continue
            
            # 新文章，添加到结果中
            idx = len(context_parts)
            seen_titles[title] = (idx, similarity)
            context_parts.append(content)
            sources.append({
                "title": title,
                "url": metadata.get("url", ""),
                "similarity": similarity,
            })

        # 限制上下文长度
        context = "\n\n".join(context_parts)
        if len(context) > self.max_context_length:
            context = context[: self.max_context_length] + "..."

        # 构建Prompt
        prompt = self._build_qa_prompt(question, context)

        # 生成答案
        try:
            answer = self.llm_service.generate(prompt)
        except Exception as e:
            log.error(f"生成答案失败: {e}")
            answer = "抱歉，生成答案时出现错误，请稍后重试。"

        return {
            "answer": answer.strip(),
            "sources": sources,
            "context": context,
        }

    def _build_qa_prompt(self, question: str, context: str) -> str:
        """
        构建问答Prompt。

        Args:
            question: 用户问题
            context: 上下文文档

        Returns:
            完整的Prompt
        """
        return f"""你是一位专业的AI助手，擅长从提供的文档内容中回答问题。

【文档内容】
{context}

【用户问题】
{question}

【要求】
1. **答案质量**：
   - 基于提供的文档内容，深入、详细地回答用户问题
   - 如果文档内容与问题相关，请综合所有相关信息，给出完整、准确的答案
   - 如果文档内容与问题部分相关，请基于相关部分回答，并说明文档的局限性
   - 答案要准确、完整、有条理
   - 使用分点或分段说明，使答案结构清晰

2. **语言要求**：
   - 使用简体中文回答
   - 语言流畅自然，专业但易懂
   - 避免使用"没有找到相关信息"等否定性表述，除非文档内容确实完全不相关

3. **引用说明**：
   - 如果信息来自文档，可以在答案中提及"根据文档内容..."或"文档中提到..."
   - 如果文档内容与问题相关但不够完整，可以说明"文档中提到了...，但关于...的内容较少"

4. **相关性处理**：
   - 如果文档内容与问题高度相关，请详细回答
   - 如果文档内容与问题部分相关，请基于相关部分回答，并说明可能需要更多信息
   - 只有在文档内容确实完全不相关时，才说明"文档内容与问题不相关"

【答案】
"""

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

