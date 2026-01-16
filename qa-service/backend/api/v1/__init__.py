# encoding: utf-8
"""API v1 路由"""

from fastapi import APIRouter

from .health import router as health_router
from .knowledge_base import router as knowledge_base_router

# 聚合所有 v1 路由
router = APIRouter(tags=["ai-demo"])

router.include_router(health_router)
router.include_router(knowledge_base_router)

__all__ = ["router"]

