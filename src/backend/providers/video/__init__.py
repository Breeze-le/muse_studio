"""Video Provider 模块

提供视频生成服务，支持多种视频生成模型。

可用提供商:
    - thirtytwo_kling: 302.AI Kling 可灵（图生视频）

示例:
    >>> from src.backend.providers.video import thirtytwo_kling
    >>> provider = thirtytwo_kling.thirtytwo_kling_provider
    >>> if provider.is_available():
    ...     video = provider.generate(
    ...         "让画面动起来，展现微妙的动态",
    ...         images=["https://example.com/image.jpg"]
    ...     )
"""

from .base import BaseVideoProvider
from .thirtytwo_kling import ThirtyTwoKlingProvider, thirtytwo_kling_provider

__all__ = [
    "BaseVideoProvider",
    "ThirtyTwoKlingProvider",
    "thirtytwo_kling_provider",
]
