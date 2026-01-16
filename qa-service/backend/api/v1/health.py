# encoding: utf-8
"""健康检查和模型列表路由"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter

from shared.config import settings
from shared.logger import log
from models import HealthResponse, ModelInfo

# 已删除 test_case 模块

router = APIRouter(tags=["health"])


@router.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    """健康检查"""
    return HealthResponse(status="ok", version=settings.app_version, name=settings.app_name)


# 已删除模型列表路由（test_case 模块已删除）

