"""Image Provider 模块

提供图片生成服务，支持多种图片生成模型。

可用提供商:
    - thirtytwo_nano_banana: 302.AI Nano-Banana (Google Nano-Banana-2)
    - thirtytwo_seedream: 302.AI Seedream (Doubao Seedream 5.0)

示例:
    >>> from src.backend.providers.image import thirtytwo_seedream
    >>> provider = thirtytwo_seedream.thirtytwo_seedream_provider
    >>> if provider.is_available():
    ...     # 文生图
    ...     image = provider.generate("一只可爱的猫咪")
    ...     # 图生图
    ...     image = provider.generate("变成卡通风格", image="https://example.com/cat.jpg")
"""

from .base import BaseImageProvider
from .thirtytwo_nano_banana import ThirtyTwoNanoBananaProvider, thirtytwo_nano_banana_provider
from .thirtytwo_seedream import ThirtyTwoSeedreamProvider, thirtytwo_seedream_provider

__all__ = [
    "BaseImageProvider",
    "ThirtyTwoNanoBananaProvider",
    "thirtytwo_nano_banana_provider",
    "ThirtyTwoSeedreamProvider",
    "thirtytwo_seedream_provider",
]
