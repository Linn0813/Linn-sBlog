# encoding: utf-8
"""
知识库服务层，封装知识库相关业务逻辑。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime
import json

from infrastructure.external.blog.loader import BlogDocumentLoader
from infrastructure.vector_store.chroma import VectorStore
from domain.knowledge_base.rag import RAGEngine
from shared.logger import log

class KnowledgeBaseService:
    """知识库服务，提供文档同步和问答功能。"""

    def __init__(self):
        """初始化知识库服务。"""
        self.document_loader = BlogDocumentLoader()
        self._rag_engine = None
        self._web_search_service = None
        # 创建结果保存目录
        project_root = Path(__file__).parent.parent.parent
        self.results_dir = project_root / 'data' / 'query_results'
        self.results_dir.mkdir(parents=True, exist_ok=True)

    @property
    def rag_engine(self) -> RAGEngine:
        """
        获取RAG引擎（延迟初始化）。
        
        Returns:
            RAG引擎实例
            
        Raises:
            ImportError: 如果缺少必要的依赖
        """
        if self._rag_engine is None:
            try:
                self._rag_engine = RAGEngine()
            except ImportError as e:
                raise ImportError(
                    f"知识库功能不可用（缺少依赖）: {e}\n"
                    "请安装依赖: pip install sentence-transformers chromadb"
                ) from e
        return self._rag_engine

    def sync_blog_posts(self, incremental: bool = True) -> Dict[str, Any]:
        """
        同步博客文章（支持增量同步）。

        Args:
            incremental: 是否使用增量同步（默认True）

        Returns:
            同步结果，包含同步的文档数量和状态
        """
        try:
            log.info(f"开始同步博客文章 (增量模式: {incremental})")

            # 加载所有博客文章
            documents = self.document_loader.load_all_posts()

            if not documents:
                return {
                    "success": False,
                    "message": "未找到文档",
                    "document_count": 0,
                    "new_count": 0,
                    "updated_count": 0,
                    "skipped_count": 0,
                }

            # 增量同步：获取已有文档
            existing_docs = {}
            if incremental:
                # 获取所有来源为 blog 的文档
                try:
                    all_docs = self.rag_engine.vector_store._collection.get(
                        where={"source": "blog"}
                    )
                    # 按文档ID分组（去除chunk后缀）
                    for doc_id, metadata in zip(all_docs.get("ids", []), all_docs.get("metadatas", [])):
                        # chunk_id格式：{post_id}_chunk_{idx}，提取post_id
                        post_id = doc_id.split("_chunk_")[0]
                        if post_id not in existing_docs:
                            existing_docs[post_id] = metadata
                except Exception as e:
                    log.warning(f"获取已有文档失败: {e}")
                log.info(f"向量库中已有 {len(existing_docs)} 个博客文章")

            # 准备文档数据（只同步新增或更新的文档）
            doc_data = []
            new_count = 0
            updated_count = 0
            skipped_count = 0
            current_doc_ids = set()

            for doc in documents:
                doc_id = doc["id"]
                current_doc_ids.add(doc_id)
                doc_date = doc["metadata"].get("date", 0)
                
                # 增量同步：检查是否需要更新
                if incremental and doc_id in existing_docs:
                    existing_date = existing_docs[doc_id].get("date", 0)
                    # 比较日期（文件修改时间）
                    if doc_date <= existing_date:
                        skipped_count += 1
                        log.debug(f"跳过未更新的文章: {doc['metadata'].get('title', '未知')}")
                        continue
                    updated_count += 1
                    log.debug(f"文章已更新: {doc['metadata'].get('title', '未知')}")
                else:
                    new_count += 1

                doc_data.append({
                    "id": doc_id,
                    "content": doc["content"],
                    "metadata": {
                        **doc["metadata"],
                        "source": "blog",
                    },
                })

            # 删除已不存在的文档（增量同步时）
            deleted_count = 0
            if incremental and existing_docs:
                deleted_ids = set(existing_docs.keys()) - current_doc_ids
                if deleted_ids:
                    log.info(f"发现 {len(deleted_ids)} 个已删除的文章，准备清理...")
                    for deleted_id in deleted_ids:
                        try:
                            # 查询该文章的所有chunk
                            all_docs = self.rag_engine.vector_store._collection.get(
                                where={"source": "blog"}
                            )
                            chunk_ids_to_delete = [
                                doc_id for doc_id in all_docs.get("ids", [])
                                if doc_id.startswith(f"{deleted_id}_chunk_") or doc_id == deleted_id
                            ]
                            if chunk_ids_to_delete:
                                self.rag_engine.vector_store.delete(ids=chunk_ids_to_delete)
                                deleted_count += 1
                                log.info(f"已删除文章: {deleted_id}")
                        except Exception as e:
                            log.warning(f"删除文章失败 {deleted_id}: {e}")

            # 如果有需要同步的文档，先删除旧版本再索引新版本
            if doc_data:
                # 先删除需要更新的文档的旧版本
                if incremental:
                    ids_to_update = {doc["id"] for doc in doc_data}
                    for doc_id in ids_to_update:
                        try:
                            all_docs = self.rag_engine.vector_store._collection.get(
                                where={"source": "blog"}
                            )
                            chunk_ids_to_delete = [
                                chunk_id for chunk_id in all_docs.get("ids", [])
                                if chunk_id.startswith(f"{doc_id}_chunk_") or chunk_id == doc_id
                            ]
                            if chunk_ids_to_delete:
                                self.rag_engine.vector_store.delete(ids=chunk_ids_to_delete)
                        except Exception as e:
                            log.warning(f"删除旧版本失败 {doc_id}: {e}")

                # 索引文档
                indexed_count = self.rag_engine.index_documents(doc_data)
            else:
                indexed_count = 0
                log.info("没有需要同步的文章")

            return {
                "success": True,
                "message": "同步成功",
                "document_count": len(documents),
                "new_count": new_count,
                "updated_count": updated_count,
                "skipped_count": skipped_count,
                "deleted_count": deleted_count,
                "indexed_count": indexed_count,
            }

        except Exception as e:
            log.error(f"同步文档失败: {e}")
            return {
                "success": False,
                "message": f"同步失败: {str(e)}",
                "document_count": 0,
                "new_count": 0,
                "updated_count": 0,
                "skipped_count": 0,
                "deleted_count": 0,
            }

    def sync_all_spaces(self, incremental: bool = True) -> Dict[str, Any]:
        """
        同步所有知识库空间。

        Args:
            incremental: 是否使用增量同步（默认True）

        Returns:
            同步结果
        """
        try:
            # 获取所有知识库空间
            spaces = self.document_loader.load_wiki_spaces()

            total_documents = 0
            total_new = 0
            total_updated = 0
            total_skipped = 0
            total_deleted = 0
            success_count = 0
            failed_spaces = []

            for space in spaces:
                space_id = space.get("space_id", "")
                space_name = space.get("name", "未知")

                if not space_id:
                    continue

                log.info(f"同步知识库空间: {space_name} ({space_id})")

                result = self.sync_documents_from_space(space_id, incremental=incremental)
                if result["success"]:
                    success_count += 1
                    total_documents += result["document_count"]
                    total_new += result.get("new_count", 0)
                    total_updated += result.get("updated_count", 0)
                    total_skipped += result.get("skipped_count", 0)
                    total_deleted += result.get("deleted_count", 0)
                else:
                    failed_spaces.append({
                        "space_id": space_id,
                        "name": space_name,
                        "error": result["message"],
                    })

            sync_mode = "增量" if incremental else "全量"
            return {
                "success": True,
                "message": f"同步完成（{sync_mode}模式）：成功 {success_count} 个，失败 {len(failed_spaces)} 个",
                "total_spaces": len(spaces),
                "success_count": success_count,
                "failed_count": len(failed_spaces),
                "total_documents": total_documents,
                "new_count": total_new,
                "updated_count": total_updated,
                "skipped_count": total_skipped,
                "deleted_count": total_deleted,
                "failed_spaces": failed_spaces,
            }

        except Exception as e:
            error_msg = str(e)
            log.error(f"同步所有知识库失败: {e}")
            
            # 检查是否是权限错误，如果是则重新抛出以便API层处理
            is_auth_error = (
                "99991672" in error_msg or 
                "99991663" in error_msg or 
                "99991664" in error_msg or 
                "99991679" in error_msg or
                "权限" in error_msg or 
                "Access denied" in error_msg or
                "unauthorized" in error_msg.lower() or
                "forbidden" in error_msg.lower()
            )
            if is_auth_error:
                raise  # 重新抛出异常，让API层返回403
            
            return {
                "success": False,
                "message": f"同步失败: {error_msg}",
                "total_spaces": 0,
                "success_count": 0,
                "failed_count": 0,
                "total_documents": 0,
            }

    @property
    def web_search_service(self):
        """获取网络搜索服务（延迟初始化）"""
        if self._web_search_service is None:
            try:
                from infrastructure.external.web_search import WebSearchService
                self._web_search_service = WebSearchService()
            except Exception as e:
                log.warning(f"网络搜索服务不可用: {e}")
                self._web_search_service = None
        return self._web_search_service

    def ask(self, question: str, space_id: Optional[str] = None, use_web_search: bool = False) -> Dict[str, Any]:
        """
        回答问题。
        
        使用向量搜索模式：使用本地向量存储进行语义搜索（需要先同步文档）

        Args:
            question: 用户问题
            space_id: 指定搜索的博客分类，如果不提供则搜索所有文章
            use_web_search: 是否启用网络搜索（默认False）。当知识库结果不理想时，会使用网络搜索补充

        Returns:
            答案和引用来源
        """
        try:
            # 检查向量存储中是否有文档
            collection_info = self.get_collection_info()
            has_local_docs = (
                collection_info.get("success") 
                and collection_info.get("info", {}).get("count", 0) > 0
            )
            
            if not has_local_docs:
                return {
                    "success": False,
                    "answer": "向量数据库中还没有博客文章，请先同步博客文章。\n\n提示：博客文章会在 `hexo generate` 时自动同步，或运行 `npm run sync-blog` 手动同步。",
                    "sources": [],
                    "suggest_web_search": True,
                    "max_similarity": 0.0,
                }
            
            # 使用向量搜索模式
            # 注意：目前向量搜索不支持按分类过滤，space_id 参数暂时忽略
            if space_id:
                log.warning(f"向量搜索暂不支持按分类过滤，将搜索所有文章（忽略分类: {space_id}）")
            result = self.rag_engine.qa(question)
                
            # 从RAG结果中获取相似度信息（RAG引擎已经计算好了）
            sources = result.get("sources", [])
            max_similarity = result.get("max_similarity", 0.0)  # 使用RAG引擎计算的max_similarity
            avg_similarity = result.get("avg_similarity", 0.0)  # 使用RAG引擎计算的avg_similarity
            
            # 如果没有从RAG结果中获取到，则从sources计算
            if max_similarity == 0.0 and sources:
                max_similarity = max([s.get("similarity", 0) for s in sources])
            
            log.info(f"问答结果 - 最高相似度: {max_similarity:.3f}, 平均相似度: {avg_similarity:.3f}, 来源数: {len(sources)}")
            
            # 构建用于判断网络搜索的result字典（确保包含所有必要字段）
            kb_result_for_search = {
                "success": len(sources) > 0,  # 有来源就认为成功
                "sources": sources,
                "answer": result.get("answer", ""),
                "max_similarity": max_similarity,
            }
                
                # 判断是否建议使用网络搜索
            suggest_web_search = self._should_use_web_search(question, kb_result_for_search)
                
                # 如果启用了网络搜索，且知识库结果不理想，尝试网络搜索
                if use_web_search and suggest_web_search:
                    log.info("🌐 知识库结果不理想，尝试使用网络搜索补充...")
                web_result = self._search_web_and_merge(question, result)
                    return web_result
                
                # 如果未启用网络搜索，但建议使用，在结果中添加建议信息
                if not use_web_search:
                result["suggest_web_search"] = suggest_web_search
                result["max_similarity"] = max_similarity
                    if suggest_web_search:
                        log.info(f"💡 建议使用网络搜索（最高相似度: {max_similarity:.3f}）")
                
            # 检查答案质量：如果答案包含否定性表述但相似度较高，记录警告
            answer = result.get("answer", "")
            negative_keywords = ["没有找到", "未找到", "不相关", "无法找到", "没有相关信息"]
            has_negative = any(keyword in answer for keyword in negative_keywords)
            
            # 如果相似度较高（>=0.7）但答案包含否定性表述，记录警告
            if max_similarity >= 0.7 and has_negative:
                log.warning(f"答案包含否定性表述，但文档相似度较高({max_similarity:.3f})，可能存在Prompt理解问题")
            
            return {
                "success": True,
                "answer": result["answer"],
                "sources": result["sources"],
                "suggest_web_search": result.get("suggest_web_search", False),
                "max_similarity": max_similarity,
                "avg_similarity": avg_similarity,
            }

        except Exception as e:
            log.error(f"回答问题失败: {e}")
            return {
                "success": False,
                "answer": f"抱歉，处理问题时出现错误: {str(e)}",
                "sources": [],
            }
    
    def get_wiki_spaces(self) -> Dict[str, Any]:
        """
        获取博客分类列表（用于兼容 get_wiki_spaces API）。
        
        Returns:
            分类列表
        """
        try:
            categories = self.document_loader.get_blog_categories()
            
            return {
                "success": True,
                "spaces": categories,
                "message": f"找到 {len(categories)} 个博客分类",
            }
        except Exception as e:
            log.error(f"获取博客分类列表失败: {e}")
                return {
                    "success": False,
                    "spaces": [],
                "message": f"获取博客分类列表失败: {str(e)}",
            }
    
    def _save_query_result(self, question: str, step: str, data: Dict[str, Any], query_timestamp: Optional[str] = None):
        """保存查询结果到文件"""
        try:
            # 如果提供了query_timestamp，使用它；否则生成新的
            if query_timestamp is None:
                query_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            filename = f"query_{query_timestamp}.json"
            filepath = self.results_dir / filename
            
            # 如果文件已存在，追加数据；否则创建新文件
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
            else:
                result_data = {
                    "question": question,
                    "timestamp": query_timestamp,
                    "steps": {}
                }
            
            result_data["steps"][step] = {
                "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "data": data
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            log.info(f"💾 查询结果已保存到: {filepath} (步骤: {step})")
            return query_timestamp  # 返回时间戳，供后续步骤使用
        except Exception as e:
            log.warning(f"保存查询结果失败: {e}")
            return None
    def _detect_question_type(self, question: str) -> Dict[str, Any]:
        """
        检测问题类型：文档列表查询 vs 内容问答
        
        Args:
            question: 用户问题
            
        Returns:
            {
                "type": "document_list" | "content_qa" | "mixed",
                "confidence": 0.0-1.0,
                "keywords": ["关键词列表"]
            }
        """
        question_lower = question.lower()
        
        # 文档列表查询的关键词模式
        list_patterns = [
            "有哪些", "哪些文档", "相关文档", "文档列表", "列出", 
            "找到", "搜索", "查找", "文档", "哪些文档",
            "什么文档", "有什么文档", "包含哪些", "涉及哪些",
            "what documents", "list", "find documents", "search documents",
            "相关", "关于.*的文档", ".*文档.*有哪些"
        ]
        
        # 统计查询的关键词
        stats_patterns = [
            "有多少", "数量", "统计", "总数", "几个", "多少文档",
            "how many", "count", "number of"
        ]
        
        # 对比查询的关键词
        comparison_patterns = [
            "对比", "区别", "差异", "比较", "vs", "versus", "和.*的区别",
            "compare", "difference", "vs"
        ]
        
        # 检查文档列表查询
        list_score = 0.0
        for pattern in list_patterns:
            if pattern in question_lower:
                list_score += 0.3
                if pattern in ["有哪些", "哪些文档", "文档列表", "list"]:
                    list_score += 0.4  # 更强的信号
        
        # 检查统计查询
        stats_score = 0.0
        for pattern in stats_patterns:
            if pattern in question_lower:
                stats_score += 0.5
        
        # 检查对比查询
        comparison_score = 0.0
        for pattern in comparison_patterns:
            if pattern in question_lower:
                comparison_score += 0.5
        
        # 提取关键词（用于后续搜索）
        keywords = self._extract_keywords(question)
        
        # 判断问题类型
        if list_score >= 0.5:
            return {
                "type": "document_list",
                "confidence": min(list_score, 1.0),
                "keywords": keywords,
                "subtype": "stats" if stats_score > 0.3 else "list"
            }
        elif stats_score >= 0.3:
            return {
                "type": "document_list",  # 统计查询也归类为文档列表
                "confidence": min(stats_score, 1.0),
                "keywords": keywords,
                "subtype": "stats"
            }
        elif comparison_score >= 0.3:
            return {
                "type": "content_qa",  # 对比查询需要内容分析
                "confidence": min(comparison_score, 1.0),
                "keywords": keywords,
                "subtype": "comparison"
            }
        else:
            # 默认是内容问答
            return {
                "type": "content_qa",
                "confidence": 0.5,
                "keywords": keywords,
                "subtype": "normal"
            }
    
    def _analyze_question_with_ai(self, question: str) -> Dict[str, Any]:
        """
        使用AI分析问题并提取搜索关键词和策略。
        
        Args:
            question: 用户问题
            
        Returns:
            包含关键词、搜索查询和相关概念的字典
        """
        try:
            from infrastructure.llm.service import LLMService
            import json
            import re
            
            llm_service = LLMService()
            
            prompt = f"""分析以下问题，提取用于搜索知识库的关键词和查询策略。

用户问题：{question}

请分析：
1. 问题的核心主题是什么？
2. 需要搜索哪些关键词？（提取2-5个最重要的关键词）
3. 有哪些同义词或相关概念？
4. 可以尝试哪些不同的搜索查询？（生成3-5个不同的搜索查询，包括原问题的不同表达方式）

请以JSON格式返回，格式如下：
{{
    "keywords": ["关键词1", "关键词2"],
    "search_queries": ["搜索查询1", "搜索查询2", "搜索查询3"],
    "related_concepts": ["相关概念1", "相关概念2"]
}}

要求：
- keywords：提取的核心关键词，去除疑问词（什么、如何、怎么等）
- search_queries：多个搜索查询，包括原问题的不同表达方式、简化版本、关键词组合等
- related_concepts：相关概念或同义词

只返回JSON，不要其他文字。
"""
            
            log.info("使用AI分析问题并提取搜索策略...")
            response = llm_service.generate(prompt)
            
            # 尝试从响应中提取JSON
            json_match = re.search(r'\{[^{}]*"keywords"[^{}]*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                # 如果没有找到JSON，尝试解析整个响应
                json_str = response.strip()
                # 移除可能的markdown代码块标记
                json_str = re.sub(r'```json\s*', '', json_str)
                json_str = re.sub(r'```\s*', '', json_str)
                json_str = json_str.strip()
            
            try:
                result = json.loads(json_str)
                
                # 验证和清理结果
                keywords = result.get("keywords", [])
                search_queries = result.get("search_queries", [])
                related_concepts = result.get("related_concepts", [])
                
                # 确保至少有一个搜索查询
                if not search_queries:
                    search_queries = [question]
                else:
                    # 确保原问题在搜索查询中
                    if question not in search_queries:
                        search_queries.insert(0, question)
                
                # 限制数量
                keywords = keywords[:5]
                search_queries = search_queries[:5]
                related_concepts = related_concepts[:3]
                
                return {
                    "keywords": keywords,
                    "search_queries": search_queries,
                    "related_concepts": related_concepts,
                }
            except json.JSONDecodeError as e:
                log.warning(f"AI返回的JSON解析失败: {e}，响应: {response[:200]}")
                # 回退到正则表达式提取关键词
                return self._fallback_extract_keywords(question)
                
        except Exception as e:
            log.warning(f"AI分析问题失败: {e}，回退到正则表达式提取")
            # 回退到正则表达式提取关键词
            return self._fallback_extract_keywords(question)
    
    def _fallback_extract_keywords(self, question: str) -> Dict[str, Any]:
        """
        回退方案：使用正则表达式提取关键词。
        
        Args:
            question: 用户问题
            
        Returns:
            包含关键词和搜索查询的字典
        """
        keywords = self._extract_keywords(question)
        search_queries = [question] + keywords[:2]
        
        return {
            "keywords": keywords,
            "search_queries": search_queries,
            "related_concepts": [],
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        从问题中提取关键词。
        
        Args:
            text: 输入文本
            
        Returns:
            关键词列表
        """
        import re
        
        # 移除标点符号，保留空格
        text_clean = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        
        keywords = []
        
        # 提取中文词汇（2-4个字符，避免提取整个问题）
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,4}', text_clean)
        keywords.extend(chinese_words)
        
        # 提取英文单词（3个字符以上）
        english_words = re.findall(r'\b[a-zA-Z]{3,}\b', text_clean)
        keywords.extend(english_words)
        
        # 过滤常见停用词和疑问词
        stop_words = {
            '什么', '如何', '怎么', '为什么', '哪个', '哪些', '这个', '那个', 
            '是', '的', '了', '在', '有', '和', '与', '或', '为',
            '是什么', '如何', '怎么', '为什么', '哪个', '哪些',
            'the', 'is', 'are', 'a', 'an', 'and', 'or', 'what', 'how', 'why'
        }
        keywords = [kw for kw in keywords if kw not in stop_words and len(kw) >= 2]
        
        # 进一步过滤：如果关键词包含停用词，尝试提取核心部分
        filtered_keywords = []
        for kw in keywords:
            # 移除常见的疑问词前缀/后缀
            kw_clean = kw
            for stop in ['什么', '如何', '怎么', '为什么', '是', '的']:
                if kw_clean.startswith(stop):
                    kw_clean = kw_clean[len(stop):]
                if kw_clean.endswith(stop):
                    kw_clean = kw_clean[:-len(stop)]
            if kw_clean and len(kw_clean) >= 2 and kw_clean not in stop_words:
                filtered_keywords.append(kw_clean)
        
        keywords = filtered_keywords if filtered_keywords else keywords
        
        # 去重（保持顺序）
        seen = set()
        unique_keywords = []
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower not in seen:
                seen.add(kw_lower)
                unique_keywords.append(kw)
        
        # 如果提取的关键词太少，尝试提取2-3字的短语
        if len(unique_keywords) < 2:
            # 提取2-3字的中文短语
            phrases = re.findall(r'[\u4e00-\u9fff]{2,3}', text)
            for phrase in phrases:
                if phrase not in stop_words and phrase not in seen:
                    seen.add(phrase.lower())
                    unique_keywords.append(phrase)
                    if len(unique_keywords) >= 3:
                        break
        
        return unique_keywords[:5]  # 最多返回5个关键词
    
    def _format_document_list(self, documents: List[Dict[str, Any]], question: str, subtype: str = "list") -> str:
        """
        格式化文档列表为答案文本。
        
        Args:
            documents: 文档列表
            question: 用户问题
            subtype: 问题子类型（list/stats）
            
        Returns:
            格式化后的答案文本
        """
        if not documents:
            return "未找到相关文档。"
        
        # 统计查询
        if subtype == "stats":
            answer = f"找到 {len(documents)} 个相关文档：\n\n"
        else:
            answer = f"找到以下 {len(documents)} 个相关文档：\n\n"
        
        # 按相似度分组（高/中/低）
        high_relevance = [d for d in documents if d.get("similarity", 0) >= 0.5]
        medium_relevance = [d for d in documents if 0.3 <= d.get("similarity", 0) < 0.5]
        low_relevance = [d for d in documents if d.get("similarity", 0) < 0.3]
        
        # 格式化文档列表
        doc_index = 1
        if high_relevance:
            answer += "**高相关性文档：**\n"
            for doc in high_relevance:
                similarity = doc.get("similarity", 0)
                similarity_str = f"（相关性: {similarity:.1%}）" if similarity > 0 else ""
                answer += f"{doc_index}. {doc['title']}{similarity_str}\n"
                doc_index += 1
            answer += "\n"
        
        if medium_relevance:
            answer += "**中等相关性文档：**\n"
            for doc in medium_relevance:
                similarity = doc.get("similarity", 0)
                similarity_str = f"（相关性: {similarity:.1%}）" if similarity > 0 else ""
                answer += f"{doc_index}. {doc['title']}{similarity_str}\n"
                doc_index += 1
            answer += "\n"
        
        if low_relevance:
            answer += "**其他相关文档：**\n"
            for doc in low_relevance:
                similarity = doc.get("similarity", 0)
                similarity_str = f"（相关性: {similarity:.1%}）" if similarity > 0 else ""
                answer += f"{doc_index}. {doc['title']}{similarity_str}\n"
                doc_index += 1
        
        # 添加提示
        answer += "\n💡 提示：点击文档标题可以查看完整内容。"
        
        return answer
    
    def _extract_relevant_chunk(self, content: str, question: str, keywords: List[str], chunk_size: int = 4000) -> str:
        """
        从文档中提取与问题最相关的片段。
        
        Args:
            content: 文档内容
            question: 用户问题
            keywords: 关键词列表
            chunk_size: 片段大小（增加到2000以提供更多上下文）
            
        Returns:
            相关片段
        """
        import re
        
        if not content:
            return ""
        
        # 如果文档较短，直接返回
        if len(content) <= chunk_size:
            return content
        
        # 按段落分割
        paragraphs = re.split(r'\n+', content)
        
        # 计算每个段落的相关性分数
        scored_paragraphs = []
        for para in paragraphs:
            if not para.strip():
                continue
            
            score = 0
            para_lower = para.lower()
            question_lower = question.lower()
            
            # 检查是否包含问题中的关键词
            for keyword in keywords:
                if keyword.lower() in para_lower:
                    score += 2
            
            # 检查是否包含问题中的完整短语
            if question_lower in para_lower:
                score += 5
            
            # 检查是否包含问题中的部分词汇
            question_words = question_lower.split()
            for word in question_words:
                if len(word) >= 2 and word in para_lower:
                    score += 1
            
            if score > 0:
                scored_paragraphs.append((score, para))
        
        # 按分数排序
        scored_paragraphs.sort(key=lambda x: x[0], reverse=True)
        
        # 选择最相关的段落组合（增加到最多15个段落，提供更多上下文）
        # 使用embedding计算段落相似度，而不是简单的关键词匹配
        selected_text = ""
        selected_count = 0
        max_paragraphs = 15  # 增加段落数量
        
        # 如果段落数量较多，尝试使用embedding计算相似度（更准确）
        if len(scored_paragraphs) > 5:
            try:
                from infrastructure.embedding.service import EmbeddingService
                import numpy as np
                
                embedding_service = EmbeddingService()
                question_vector = np.array(embedding_service.embed_text(question))
                
                # 重新计算每个段落的相似度分数（结合关键词匹配和语义相似度）
                enhanced_scored_paragraphs = []
                for score, para in scored_paragraphs[:20]:  # 只处理前20个段落以提高性能
                    # 计算语义相似度
                    para_vector = np.array(embedding_service.embed_text(para[:500]))
                    semantic_score = np.dot(question_vector, para_vector) / (
                        np.linalg.norm(question_vector) * np.linalg.norm(para_vector) + 1e-8
                    )
                    # 结合关键词匹配分数和语义相似度分数
                    combined_score = score * 0.4 + semantic_score * 100 * 0.6
                    enhanced_scored_paragraphs.append((combined_score, para))
                
                # 重新排序
                enhanced_scored_paragraphs.sort(key=lambda x: x[0], reverse=True)
                scored_paragraphs = enhanced_scored_paragraphs
            except Exception as e:
                log.debug(f"使用embedding计算相似度失败，回退到关键词匹配: {e}")
                # 如果失败，继续使用原来的关键词匹配结果
        
        # 选择段落时，保留上下文窗口（每个相关段落前后各保留一个段落）
        selected_indices = set()
        
        # 构建段落到索引的映射（用于快速查找）
        para_to_index = {}
        for idx, orig_para in enumerate(paragraphs):
            if orig_para.strip():
                para_key = orig_para.strip()[:100]  # 使用前100字符作为key
                if para_key not in para_to_index:
                    para_to_index[para_key] = []
                para_to_index[para_key].append(idx)
        
        # 选择最相关的段落及其上下文
        for score, para in scored_paragraphs[:max_paragraphs]:
            # 找到这个段落在原文中的索引
            para_key = para.strip()[:100]
            para_indices = para_to_index.get(para_key, [])
            
            if para_indices:
                # 使用第一个匹配的索引
                para_index = para_indices[0]
                # 选择当前段落及其前后各一个段落（上下文窗口）
                for ctx_idx in range(max(0, para_index - 1), min(len(paragraphs), para_index + 2)):
                    selected_indices.add(ctx_idx)
            else:
                # 如果找不到精确匹配，尝试模糊匹配
                para_stripped = para.strip()
                for idx, orig_para in enumerate(paragraphs):
                    if orig_para.strip() and para_stripped[:50] in orig_para.strip():
                        para_index = idx
                        # 选择当前段落及其前后各一个段落
                        for ctx_idx in range(max(0, para_index - 1), min(len(paragraphs), para_index + 2)):
                            selected_indices.add(ctx_idx)
                        break
        
        # 按顺序提取选中的段落
        for idx in sorted(selected_indices):
            para = paragraphs[idx]
            if not para.strip():
                continue
            
            if len(selected_text) + len(para) <= chunk_size:
                selected_text += para + "\n\n"
            else:
                # 如果超过长度限制，尝试截取部分
                remaining = chunk_size - len(selected_text)
                if remaining > 200:  # 至少保留200字符
                    selected_text += para[:remaining] + "..."
                break
        
        # 如果没有找到相关段落，返回开头部分（增加长度）
        if not selected_text:
            # 返回更多内容，包括文档开头
            selected_text = content[:chunk_size] + "..."
        
        return selected_text.strip()
    
    def _calculate_similarity(self, question: str, content: str) -> float:
        """
        计算问题和文档内容的相似度（使用embedding）。
        
        Args:
            question: 用户问题
            content: 文档内容
            
        Returns:
            相似度分数（0-1）
        """
        try:
            from infrastructure.embedding.service import EmbeddingService
            import numpy as np
            
            # 初始化embedding服务
            embedding_service = EmbeddingService()
            
            # 向量化问题和内容
            # 注意：content应该是已经提取的相关片段，不需要再截取前500字符
            # 如果content太长（超过2000字符），截取前2000字符以提高性能
            content_to_embed = content[:2000] if len(content) > 2000 else content
            
            # 确保内容不为空
            if not content_to_embed or not content_to_embed.strip():
                log.warning(f"内容为空，返回相似度0.0")
                return 0.0
            
            # 记录embedding服务信息
            model_name = embedding_service.get_model_name()
            log.debug(f"使用embedding模型: {model_name}")
            
            # 向量化问题
            question_vector_raw = embedding_service.embed_text(question)
            question_vector = np.array(question_vector_raw)
            
            # 向量化内容
            content_vector_raw = embedding_service.embed_text(content_to_embed)
            content_vector = np.array(content_vector_raw)
            
            # 验证向量是否有效
            if question_vector.size == 0 or content_vector.size == 0:
                log.warning(f"向量为空，返回相似度0.0 (question_size={question_vector.size}, content_size={content_vector.size})")
                return 0.0
            
            # 检查向量维度是否匹配
            if question_vector.shape != content_vector.shape:
                log.error(f"向量维度不匹配: question={question_vector.shape}, content={content_vector.shape}")
                return 0.0
            
            # 检查向量是否全为零
            if np.all(question_vector == 0) or np.all(content_vector == 0):
                log.warning(f"检测到零向量: question_all_zero={np.all(question_vector == 0)}, content_all_zero={np.all(content_vector == 0)}")
                log.warning(f"问题向量前5个值: {question_vector[:5]}")
                log.warning(f"内容向量前5个值: {content_vector[:5]}")
                # 如果向量全为零，使用关键词匹配作为回退
                keywords = self._extract_keywords(question)
                content_lower = content.lower() if content else ""
                match_count = sum(1 for kw in keywords if kw.lower() in content_lower)
                estimated_similarity = min(0.4, 0.1 + match_count * 0.05)
                log.info(f"检测到零向量，使用关键词匹配估计相似度: {estimated_similarity:.3f} (匹配关键词数: {match_count})")
                return estimated_similarity
            
            # 计算余弦相似度
            dot_product = np.dot(question_vector, content_vector)
            norm_q = np.linalg.norm(question_vector)
            norm_c = np.linalg.norm(content_vector)
            
            if norm_q == 0 or norm_c == 0:
                log.warning(f"向量模长为0，返回相似度0.0 (norm_q={norm_q}, norm_c={norm_c})")
                return 0.0
            
            similarity = dot_product / (norm_q * norm_c)
            
            # 🔴 修复：处理负数相似度
            # 余弦相似度范围是-1到1，负数表示向量方向相反或接近垂直
            # 负数相似度应该被视为低相关性，但不应该被直接截断为0.0
            if similarity < 0:
                # 负数相似度表示不相关，设为0.0
                # 但记录日志以便排查问题
                log.debug(f"检测到负数相似度: {similarity:.3f} (问题: {question[:50]}..., 内容长度: {len(content_to_embed)})")
                log.debug(f"点积: {dot_product:.3f}, norm_q: {norm_q:.3f}, norm_c: {norm_c:.3f}")
                similarity = 0.0
            else:
            # 确保相似度在0-1范围内
                similarity = min(1.0, float(similarity))
            
            # 添加调试日志（仅在相似度异常时）
            if similarity < 0.1:
                log.debug(f"相似度较低: {similarity:.3f} (问题: {question[:50]}..., 内容长度: {len(content_to_embed)}, 向量维度: {question_vector.shape[0]})")
                log.debug(f"问题向量统计: min={question_vector.min():.3f}, max={question_vector.max():.3f}, mean={question_vector.mean():.3f}")
                log.debug(f"内容向量统计: min={content_vector.min():.3f}, max={content_vector.max():.3f}, mean={content_vector.mean():.3f}")
            
            return similarity
            
        except Exception as e:
            log.error(f"计算相似度失败: {e}，使用关键词匹配估计值")
            import traceback
            log.debug(traceback.format_exc())
            # 如果计算失败，基于关键词匹配返回一个估计值（但标记为低相似度）
            keywords = self._extract_keywords(question)
            content_lower = content.lower() if content else ""
            match_count = sum(1 for kw in keywords if kw.lower() in content_lower)
            # 降低默认值，避免误判为相关
            estimated_similarity = min(0.4, 0.1 + match_count * 0.05)  # 基础分数0.1，每个关键词匹配+0.05，最高0.4
            log.info(f"使用关键词匹配估计相似度: {estimated_similarity:.3f} (匹配关键词数: {match_count})")
            return estimated_similarity
    
    def _analyze_search_results_with_ai(
        self, 
        question: str, 
        search_results: List[Dict[str, Any]], 
        keywords: List[str],
        related_concepts: List[str]
    ) -> Dict[str, Any]:
        """
        使用AI分析搜索结果的相关性和关键信息。
        
        Args:
            question: 用户问题
            search_results: 搜索结果列表
            keywords: 提取的关键词
            related_concepts: 相关概念
            
        Returns:
            分析结果，包含：
            - relevance_summary: 相关性总结
            - key_points: 关键信息点
            - answer_strategy: 答案生成策略
        """
        try:
            from infrastructure.llm.service import LLMService
            import json
            import re
            
            llm_service = LLMService()
            
            # 构建搜索结果摘要（只包含标题和相似度，避免token过多）
            results_summary = []
            for i, result in enumerate(search_results[:5], 1):
                results_summary.append({
                    "序号": i,
                    "标题": result.get("title", "未知"),
                    "相似度": f"{result.get('similarity', 0):.2f}",
                    "内容摘要": result.get("content", "")[:200] + "..." if len(result.get("content", "")) > 200 else result.get("content", "")
                })
            
            prompt = f"""你是一位专业的AI助手，需要分析搜索结果与用户问题的相关性。

【用户问题】
{question}

【提取的关键词】
{', '.join(keywords) if keywords else '无'}

【相关概念】
{', '.join(related_concepts) if related_concepts else '无'}

【搜索结果】
{json.dumps(results_summary, ensure_ascii=False, indent=2)}

请分析：
1. 这些搜索结果与用户问题的相关性如何？
2. 哪些结果最相关？为什么？
3. 从这些结果中可以提取哪些关键信息点？
4. 应该如何组织答案？（直接回答、分点说明、对比说明等）

请以JSON格式返回：
{{
    "relevance_summary": "相关性总结（1-2句话）",
    "key_points": ["关键信息点1", "关键信息点2", "关键信息点3"],
    "answer_strategy": "答案生成策略（如：直接回答、分点说明、对比说明等）",
    "most_relevant_results": [1, 2]  // 最相关的结果序号列表
}}

只返回JSON，不要其他文字。
"""
            
            log.info("使用AI分析搜索结果...")
            response = llm_service.generate(prompt)
            
            # 尝试从响应中提取JSON
            json_match = re.search(r'\{[^{}]*"relevance_summary"[^{}]*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response.strip()
                json_str = re.sub(r'```json\s*', '', json_str)
                json_str = re.sub(r'```\s*', '', json_str)
                json_str = json_str.strip()
            
            try:
                result = json.loads(json_str)
                return result
            except json.JSONDecodeError as e:
                log.warning(f"AI分析结果JSON解析失败: {e}，响应: {response[:200]}")
                return {
                    "relevance_summary": "搜索结果与问题相关",
                    "key_points": [],
                    "answer_strategy": "直接回答",
                    "most_relevant_results": [1, 2, 3],
                }
                
        except Exception as e:
            log.warning(f"AI分析搜索结果失败: {e}")
            return {
                "relevance_summary": "搜索结果与问题相关",
                "key_points": [],
                "answer_strategy": "直接回答",
                "most_relevant_results": [1, 2, 3],
            }
    
    def _build_answer_prompt(
        self,
        question: str,
        context: str,
        search_results: List[Dict[str, Any]],
        analysis_result: Dict[str, Any],
        keywords: List[str]
    ) -> str:
        """
        构建答案生成的Prompt，让AI更好地利用搜索结果。
        
        Args:
            question: 用户问题
            context: 文档上下文
            search_results: 搜索结果列表
            analysis_result: AI分析结果
            keywords: 关键词列表
            
        Returns:
            完整的Prompt
        """
        # 构建搜索结果信息
        results_info = []
        for i, result in enumerate(search_results, 1):
            similarity = result.get("similarity", 0)
            title = result.get("title", "未知")
            results_info.append(f"{i}. {title} (相似度: {similarity:.2f})")
        
        results_summary = "\n".join(results_info)
        
        # 获取AI分析的关键信息
        relevance_summary = analysis_result.get("relevance_summary", "")
        key_points = analysis_result.get("key_points", [])
        answer_strategy = analysis_result.get("answer_strategy", "直接回答")
        most_relevant = analysis_result.get("most_relevant_results", [])
        
        # 构建关键信息点
        key_points_text = ""
        if key_points:
            key_points_text = "\n".join([f"- {point}" for point in key_points[:5]])
        
        # 构建最相关结果提示
        most_relevant_text = ""
        if most_relevant:
            most_relevant_titles = [
                search_results[i-1].get("title", "") 
                for i in most_relevant 
                if 1 <= i <= len(search_results)
            ]
            if most_relevant_titles:
                most_relevant_text = f"\n【最相关文档】优先参考以下文档：{', '.join(most_relevant_titles)}"
        
        prompt = f"""你是一位资深的AI知识库助手，擅长深入分析文档内容并生成高质量、结构化的答案。

【任务】
基于提供的文档内容，深入分析并回答用户的问题。你需要：
1. **深入理解**：仔细阅读文档内容，理解上下文和细节
2. **提取关键信息**：识别与问题相关的核心信息、关键步骤、重要概念
3. **综合分析**：如果涉及多个文档，要综合不同文档的信息，形成完整的答案
4. **结构化组织**：按照逻辑顺序组织答案，使用清晰的段落和分点说明
5. **深入阐述**：不仅要引用文档内容，还要进行解释、分析和总结

【用户问题】
{question}

【提取的关键词】
{', '.join(keywords) if keywords else '无'}

【搜索结果分析】
{relevance_summary if relevance_summary else '搜索结果与问题相关'}

【关键信息点】
{key_points_text if key_points_text else '需要从文档中提取'}

【答案生成策略】
{answer_strategy}{most_relevant_text}

【文档内容】
{context}

【搜索结果列表】
{results_summary}

【核心要求】
1. **深度分析**：
   - 不要简单引用文档中的一两句话
   - 要深入理解文档内容，提取关键信息并进行解释
   - 如果文档提到某个功能或概念，要详细说明其作用、使用方法、注意事项等

2. **完整性**：
   - 如果文档中有多个相关信息点，要全部提取并综合回答
   - 不要遗漏重要的细节、步骤、条件、限制等
   - 如果涉及多个方面，要全面覆盖

3. **结构化组织**：
   - 使用清晰的段落结构
   - 对于复杂问题，使用分点说明（1. 2. 3.）或分类说明
   - 按照逻辑顺序组织：概述 → 详细说明 → 总结

4. **可读性和专业性**：
   - 使用简体中文，语言流畅自然
   - 使用专业术语，但确保易于理解
   - 避免冗余和重复
   - 适当使用过渡词，使答案连贯

5. **引用和标注**：
   - 在答案开头或关键部分提及文档来源（如"根据《XXX文档》..."）
   - 如果信息来自多个文档，可以分别标注

【答案结构建议】
- **开头**：简要说明找到了哪些相关信息（可提及文档名称）
- **主体**：详细回答问题的各个方面，使用分点或分段说明
- **结尾**：如有必要，进行总结或补充说明

【注意事项】
- **相关性检查（最重要）**：
  - 首先判断文档内容是否真的与用户问题相关
  - 如果文档内容与问题**完全不相关**或**相关性很低**（相似度<0.5），必须明确说明"根据提供的文档，没有找到与问题相关的信息"
  - **不要**强行关联不相关的内容
  - **不要**基于不相关的文档生成答案
  - 如果文档相似度很低，应该明确拒绝回答，而不是强行生成答案

- 如果文档中没有直接回答问题的信息，可以基于相关内容进行合理推断，但要说明这是基于文档的推断
- 如果文档内容与问题不完全匹配，说明文档中找到了哪些相关信息，并解释这些信息如何帮助回答问题
- 如果多个文档有冲突信息，要对比说明并指出差异
- 如果文档中没有相关信息，明确说明"根据提供的文档，没有找到相关信息"

【答案】
请基于以上文档内容，深入分析并回答用户问题。要求答案完整、深入、有条理：
"""
        
        return prompt

    def _verify_answer_relevance(self, question: str, answer: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        验证答案是否真的回答了用户的问题。
        
        Args:
            question: 用户问题
            answer: 生成的答案
            search_results: 搜索结果列表
            
        Returns:
            验证结果，包含is_relevant和reason
        """
        try:
            # 如果搜索结果的平均相似度很低，直接认为不相关
            if search_results:
                avg_similarity = sum([r.get("similarity", 0) for r in search_results]) / len(search_results)
                if avg_similarity < 0.4:
                    return {
                        "is_relevant": False,
                        "reason": f"搜索结果平均相似度过低 ({avg_similarity:.3f} < 0.4)"
                    }
            
            # 提取问题关键词
            question_keywords = self._extract_keywords(question)
            if not question_keywords:
                return {"is_relevant": True, "reason": "无法提取问题关键词"}
            
            # 检查答案是否包含问题的主要关键词
            answer_lower = answer.lower()
            matched_keywords = [kw for kw in question_keywords if kw.lower() in answer_lower]
            match_ratio = len(matched_keywords) / len(question_keywords) if question_keywords else 0
            
            # 如果匹配的关键词少于50%，认为不相关
            if match_ratio < 0.5:
                return {
                    "is_relevant": False,
                    "reason": f"答案中匹配的关键词比例过低 ({match_ratio:.2%} < 50%)"
                }
            
            return {"is_relevant": True, "reason": "答案相关性验证通过"}
            
        except Exception as e:
            log.warning(f"答案相关性验证失败: {e}")
            # 验证失败时，默认认为相关（避免误判）
            return {"is_relevant": True, "reason": f"验证过程出错: {e}"}
    
    def _should_use_web_search(self, question: str, kb_result: Dict[str, Any]) -> bool:
        """
        判断是否需要使用网络搜索。
        
        Args:
            question: 用户问题
            kb_result: 知识库搜索结果
            
        Returns:
            是否需要网络搜索
        """
        # 如果知识库搜索成功且有相关文档，检查相似度
        if kb_result.get("success") and len(kb_result.get("sources", [])) > 0:
            sources = kb_result.get("sources", [])
            max_similarity = kb_result.get("max_similarity", 0.0)
            
            # 如果没有max_similarity，从sources计算
            if max_similarity == 0.0:
            max_similarity = max([s.get("similarity", 0) for s in sources])
            
            # 如果最高相似度>=0.7，认为知识库结果足够好，不需要网络搜索
            if max_similarity >= 0.7:
                return False
            
            # 如果相似度在0.6-0.7之间，检查答案质量
            if max_similarity >= 0.6:
                # 检查答案是否包含否定性表述
                answer = kb_result.get("answer", "")
                negative_keywords = ["没有找到", "未找到", "不相关", "无法找到", "没有相关信息"]
                has_negative = any(keyword in answer for keyword in negative_keywords)
                
                # 如果答案包含否定性表述，建议使用网络搜索
                if has_negative:
                    log.info(f"答案包含否定性表述，且文档相似度中等({max_similarity:.3f})，建议使用网络搜索")
                    return True
                
                # 判断是否是通用概念问题（如"是什么"、"定义"等）
                if self._is_general_concept_question(question):
                    log.info(f"检测到通用概念问题，且文档相似度中等({max_similarity:.3f})，建议使用网络搜索")
                    return True
                
                return False
            
            # 如果相似度在0.5-0.6之间，判断是否是通用概念问题
            if max_similarity >= 0.5:
                # 判断是否是通用概念问题（如"是什么"、"定义"等）
                if self._is_general_concept_question(question):
                    log.info(f"检测到通用概念问题，且文档相似度较低({max_similarity:.3f})，建议使用网络搜索")
                    return True
            
            # 如果相似度<0.5，建议使用网络搜索
            if max_similarity < 0.5:
                log.info(f"文档相似度过低({max_similarity:.3f})，建议使用网络搜索")
                return True
        
        # 如果知识库搜索失败或没有找到文档，建议使用网络搜索
        if not kb_result.get("success") or len(kb_result.get("sources", [])) == 0:
            log.info("知识库未找到相关文档，建议使用网络搜索")
            return True
        
        return False
    
    def _is_general_concept_question(self, question: str) -> bool:
        """
        判断是否是通用概念问题。
        
        Args:
            question: 用户问题
            
        Returns:
            是否是通用概念问题
        """
        # 通用概念问题的关键词
        concept_keywords = [
            "是什么", "什么是", "定义", "含义", "意思", "概念",
            "介绍", "说明", "解释", "如何理解", "怎么理解"
        ]
        
        question_lower = question.lower()
        for keyword in concept_keywords:
            if keyword in question_lower:
                return True
        
        return False
    
    def _search_web_and_merge(self, question: str, kb_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        搜索网络并合并结果。
        
        Args:
            question: 用户问题
            kb_result: 知识库搜索结果
            
        Returns:
            合并后的结果
        """
        try:
            web_service = self.web_search_service
            if not web_service:
                log.warning("网络搜索服务不可用，返回知识库结果")
                return kb_result
            
            # 搜索网络
            web_results = web_service.search(question, max_results=5)
            
            if not web_results:
                log.warning("网络搜索未找到结果，返回知识库结果")
                return kb_result
            
            # 使用LLM合并知识库和网络搜索结果
            from infrastructure.llm.service import LLMService
            llm_service = LLMService()
            
            # 构建合并提示词
            kb_answer = kb_result.get("answer", "")
            kb_sources = kb_result.get("sources", [])
            
            # 构建网络搜索结果摘要
            web_summary = "\n".join([
                f"- {r.get('title', '')}: {r.get('snippet', '')[:200]}..."
                for r in web_results[:3]
            ])
            
            # 构建合并提示词
            prompt = f"""你是一位专业的AI助手，需要结合知识库信息和网络搜索结果来回答用户问题。

【用户问题】
{question}

【知识库信息】
{'找到了以下相关文档：' if kb_sources else '未找到相关文档'}
{chr(10).join([f'- {s.get("title", "")} (相似度: {s.get("similarity", 0):.2f})' for s in kb_sources[:3]]) if kb_sources else '无'}

{'【知识库答案】' if kb_answer and kb_result.get('success') else ''}
{kb_answer if kb_answer and kb_result.get('success') else '知识库未找到相关信息'}

【网络搜索结果】
{web_summary}

【要求】
1. 优先使用知识库信息（如果知识库有相关信息）
2. 使用网络搜索结果补充知识库信息的不足
3. 明确标注信息来源：
   - 如果信息来自知识库，标注"根据知识库文档..."
   - 如果信息来自网络搜索，标注"根据网络搜索..."
4. 如果知识库和网络信息有冲突，优先使用知识库信息
5. 答案要完整、准确、有条理
6. 使用简体中文回答

【答案】
请结合以上信息，回答用户问题：
"""
            
            # 生成合并后的答案
            merged_answer = llm_service.generate(prompt)
            
            # 合并来源
            merged_sources = list(kb_sources)
            for web_result in web_results[:3]:
                merged_sources.append({
                    "title": web_result.get("title", ""),
                    "url": web_result.get("url", ""),
                    "source": "web_search",
                    "similarity": 0.0,  # 网络搜索结果没有相似度
                })
            
            # 保存网络搜索结果
            query_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self._save_query_result(question, "web_search", {
                "results_count": len(web_results),
                "results": web_results[:5]
            }, query_timestamp)
            
            log.info("✅ 网络搜索结果已合并到答案中")
            
            return {
                "success": True,
                "answer": merged_answer.strip(),
                "sources": merged_sources,
                "has_web_search": True,  # 标记使用了网络搜索
                "suggest_web_search": False,  # 已经使用了，不再建议
                "max_similarity": max([s.get("similarity", 0) for s in kb_sources]) if kb_sources else 0.0,
            }
            
        except Exception as e:
            log.error(f"网络搜索和合并失败: {e}")
            # 如果网络搜索失败，返回知识库结果
            return kb_result
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        获取向量存储信息。

        Returns:
            集合信息
        """
        try:
            info = self.rag_engine.vector_store.get_collection_info()
            return {
                "success": True,
                "info": info,
            }
        except Exception as e:
            log.error(f"获取集合信息失败: {e}")
            return {
                "success": False,
                "info": {},
            }

