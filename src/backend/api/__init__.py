"""
API 路由模块

提供 Provider 相关的 RESTful API 端点。
"""

from .providers import router as providers_router

__all__ = ["providers_router"]
