# encoding: utf-8
"""知识库路由"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from shared.config import settings
from shared.logger import log
from models import (
    AskQuestionRequest,
    AskQuestionResponse,
    CollectionInfoResponse,
    SyncDocumentsRequest,
    SyncDocumentsResponse,
    WikiSpacesResponse,
)

# 知识库服务（可选，如果依赖未安装则跳过）
try:
    from domain.knowledge_base.service import KnowledgeBaseService
    KNOWLEDGE_BASE_AVAILABLE = True
except ImportError as e:
    KNOWLEDGE_BASE_AVAILABLE = False
    KnowledgeBaseService = None
    import warnings
    warnings.warn(
        f"知识库功能不可用（缺少依赖）: {e}\n"
        "如果需要使用知识库功能，请安装: pip install sentence-transformers chromadb",
        ImportWarning
    )

router = APIRouter(tags=["knowledge-base"])


# ==================== 知识库路由 ====================

def _check_knowledge_base_available():
    """检查知识库功能是否可用"""
    if not KNOWLEDGE_BASE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="知识库功能不可用，请安装依赖: pip install sentence-transformers chromadb"
        )


def _get_knowledge_base_service():
    """获取知识库服务实例"""
    _check_knowledge_base_available()
    service = KnowledgeBaseService()
    _ = service.rag_engine  # 触发延迟初始化，如果缺少依赖会抛出ImportError
    return service


@router.post("/knowledge-base/sync", response_model=SyncDocumentsResponse)
def sync_documents(payload: SyncDocumentsRequest) -> SyncDocumentsResponse:
    """
    同步知识库文档到向量存储。
    
    Args:
        payload: 同步请求，包含知识库空间ID（可选）
    
    Returns:
        同步结果
    """
    try:
        service = _get_knowledge_base_service()
        
        # 同步博客文章（忽略 space_id 参数）
        result = service.sync_blog_posts(incremental=payload.incremental)
        
        return SyncDocumentsResponse(**result)
    except ImportError as exc:
        log.warning(f"知识库依赖未安装: {exc}")
        raise HTTPException(
            status_code=503,
            detail=f"知识库功能不可用，请安装依赖: pip install sentence-transformers chromadb"
        ) from exc
    except Exception as exc:  # noqa: BLE001
        log.exception("同步知识库文档失败")
        raise HTTPException(status_code=500, detail=f"同步知识库文档失败: {exc}") from exc


@router.post("/knowledge-base/ask", response_model=AskQuestionResponse)
def ask_question(payload: AskQuestionRequest) -> AskQuestionResponse:
    """
    回答用户问题（基于知识库）。
    
    Args:
        payload: 问答请求，包含用户问题和可选的知识库空间ID
    
    Returns:
        答案和引用来源
    """
    try:
        service = _get_knowledge_base_service()
        result = service.ask(
            payload.question, 
            space_id=payload.space_id,
            use_web_search=payload.use_web_search
        )
        
        # 转换sources格式
        sources = []
        for s in result.get("sources", []):
            source_info = {
                "title": s["title"],
                "url": s["url"],
            }
            if s.get("source") == "web_search":
                source_info["similarity"] = 0.0
            else:
                source_info["similarity"] = s.get("similarity", 0.0)
            sources.append(source_info)
        
        return AskQuestionResponse(
            success=result["success"],
            answer=result["answer"],
            sources=sources,
            has_web_search=result.get("has_web_search", False),
            suggest_web_search=result.get("suggest_web_search", False),
            max_similarity=result.get("max_similarity"),
        )
    except ImportError as exc:
        log.warning(f"知识库依赖未安装: {exc}")
        raise HTTPException(
            status_code=503,
            detail=f"知识库功能不可用，请安装依赖: pip install sentence-transformers chromadb"
        ) from exc
    except Exception as exc:  # noqa: BLE001
        log.exception("回答问题失败")
        raise HTTPException(status_code=500, detail=f"回答问题失败: {exc}") from exc


@router.get("/knowledge-base/info", response_model=CollectionInfoResponse)
def get_collection_info() -> CollectionInfoResponse:
    """
    获取向量存储集合信息。
    
    Returns:
        集合信息
    """
    try:
        service = _get_knowledge_base_service()
        result = service.get_collection_info()
        return CollectionInfoResponse(**result)
    except ImportError as exc:
        log.warning(f"知识库依赖未安装: {exc}")
        raise HTTPException(
            status_code=503,
            detail=f"知识库功能不可用，请安装依赖: pip install sentence-transformers chromadb"
        ) from exc
    except Exception as exc:  # noqa: BLE001
        log.exception("获取集合信息失败")
        raise HTTPException(status_code=500, detail=f"获取集合信息失败: {exc}") from exc


@router.get("/knowledge-base/spaces", response_model=WikiSpacesResponse)
def get_wiki_spaces() -> WikiSpacesResponse:
    """
    获取所有知识库空间列表。
    
    Returns:
        知识库空间列表
    """
    try:
        service = _get_knowledge_base_service()
        result = service.get_wiki_spaces()
        return WikiSpacesResponse(**result)
    except ImportError as exc:
        log.warning(f"知识库依赖未安装: {exc}")
        raise HTTPException(
            status_code=503,
            detail=f"知识库功能不可用，请安装依赖: pip install sentence-transformers chromadb"
        ) from exc
    except Exception as exc:  # noqa: BLE001
        log.exception("获取知识库空间列表失败")
        raise HTTPException(status_code=500, detail=f"获取知识库空间列表失败: {exc}") from exc

