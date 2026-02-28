"""302.AI Nano-Banana 图片生成提供商

使用 302.AI 的 Google Nano-Banana-2 模型生成图片。

API 文档:
    - 文生图: https://doc.302.ai/420136730e0
    - 图生图: https://doc.302.ai/420136731e0

价格:
    分辨率1K/2K 0.08 PTC/次
    分辨率4K 0.16 PTC/次

环境变量:
    THIRTYTWO_GEMINI_IMAGE_API_KEY: 302.AI Gemini 图片 API 密钥（优先）
    THIRTYTWO_API_KEY: 302.AI 通用 API 密钥（备选）
    THIRTYTWO_IMAGE_MODEL: 图片生成模型名称

示例:
    >>> provider = ThirtyTwoNanoBananaProvider()
    >>> if provider.is_available():
    ...     # 文生图
    ...     image = provider.generate("一只可爱的猫咪")
    ...     # 图生图
    ...     image = provider.generate("变成卡通风格", images=["https://example.com/cat.jpg"])
"""

import requests
from src.backend.config import config
from src.backend.logger import logger
from .base import BaseImageProvider


class ThirtyTwoNanoBananaProvider(BaseImageProvider):
    """302.AI Nano-Banana 图片生成提供商

    使用 302.AI 的图片生成模型生成图片。

    特性:
        - 同步按次收费模式
        - 支持文生图（text-to-image）
        - 支持图生图（image-to-image）
        - 支持 1K/2K/4K 分辨率
        - 支持自定义宽高比
        - 返回图片二进制数据

    Attributes:
        api_base_text_to_image: 文生图 API 端点
        api_base_image_to_image: 图生图 API 端点
        default_resolution: 默认分辨率

    可用模型:
        Google Nano-Banana 系列:
            - google/nano-banana-2           # Nano-Banana-2（默认，性价比高）
            - google/nano-banana-pro         # Nano-Banana-Pro（更高质量）
            - google/nano-banana             # Nano-Banana（轻量版）
        Google Imagen 系列:
            - google/imagen-4-preview-ultra  # Imagen 4 Ultra（最高质量）
            - google/imagen-4-preview-fast   # Imagen 4 Fast（快速生成）
            - google/imagen-3-fast           # Imagen 3 Fast
    """

    API_BASE_TEXT_TO_IMAGE = "https://api.302.ai/ws/api/v3/google/nano-banana-2/text-to-image"
    API_BASE_IMAGE_TO_IMAGE = "https://api.302.ai/ws/api/v3/google/nano-banana-2/edit"

    def __init__(self):
        super().__init__(
            api_key=config.THIRTYTWO_GEMINI_IMAGE_API_KEY or config.THIRTYTWO_API_KEY or "",
            model_name=config.THIRTYTWO_IMAGE_MODEL
        )
        self.api_base_text_to_image = self.API_BASE_TEXT_TO_IMAGE
        self.api_base_image_to_image = self.API_BASE_IMAGE_TO_IMAGE
        self.default_resolution = "2k"

        if self.api_key:
            self.client = True
            logger.info(f"ThirtyTwoNanoBananaProvider initialized with model: {self.model_name}")
        else:
            self.client = None
            logger.debug("ThirtyTwoNanoBananaProvider not initialized - THIRTYTWO_GEMINI_IMAGE_API_KEY or THIRTYTWO_API_KEY not configured")

    def generate(
        self,
        prompt: str,
        images: list[str] | None = None,
        resolution: str = "2k",
        aspect_ratio: str = "3:4",
        enable_base64_output: bool = False,
        enable_sync_mode: bool = True,
        **kwargs
    ) -> bytes:
        """生成图片

        Args:
            prompt: 图片描述提示词（必填）
            images: 参考图片 URL 列表，用于图生图功能
                    当提供此参数时，将使用图片编辑接口
            resolution: 图片分辨率，可选值: "1k", "2k", "4k"
            aspect_ratio: 宽高比，如 "3:4", "1:1", "16:9"
            enable_base64_output: 是否返回 base64 编码的图片数据
            enable_sync_mode: 是否启用同步模式
            **kwargs: 其他厂商特定参数

        Returns:
            bytes: 图片二进制数据

        Raises:
            ValueError: API 密钥未配置
            RuntimeError: API 请求失败

        示例:
            >>> provider = ThirtyTwoNanoBananaProvider()
            >>> # 文生图
            >>> image = provider.generate("一只柯基犬在草地上奔跑")
            >>> # 图生图
            >>> image = provider.generate(
            ...     "变成卡通风格",
            ...     images=["https://example.com/dog.jpg"]
            ... )
        """
        if not self.is_available():
            raise ValueError("ThirtyTwoNanoBananaProvider not available - check THIRTYTWO_GEMINI_IMAGE_API_KEY or THIRTYTWO_API_KEY")

        # 根据是否提供 images 参数选择 API 端点
        if images:
            api_url = self.api_base_image_to_image
        else:
            api_url = self.api_base_text_to_image

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "prompt": prompt,
            "resolution": resolution or self.default_resolution,
            "aspect_ratio": aspect_ratio,
            "enable_base64_output": enable_base64_output,
            "enable_sync_mode": enable_sync_mode,
        }

        # 添加图片参数（图生图）
        if images:
            payload["images"] = images

        # 添加额外的参数
        payload.update(kwargs)

        try:
            logger.info(f"Generating image with prompt: {prompt[:50]}... (mode: {'image-to-image' if images else 'text-to-image'})")

            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()

            data = response.json()

            if data.get("code") == 200:
                outputs = data.get("data", {}).get("outputs", [])
                if outputs and isinstance(outputs, list):
                    image_url = outputs[0]
                    logger.info(f"Image generated successfully: {image_url}")

                    # 下载图片并返回二进制数据
                    img_response = requests.get(image_url, timeout=60)
                    img_response.raise_for_status()
                    return img_response.content
                else:
                    raise RuntimeError("No image URL in response")
            else:
                error_msg = data.get("message", "Unknown error")
                raise RuntimeError(f"API error: {error_msg}")

        except requests.RequestException as e:
            logger.error(f"HTTP error during image generation: {e}")
            raise RuntimeError(f"HTTP error: {e}") from e
        except Exception as e:
            logger.error(f"Error during image generation: {e}")
            raise RuntimeError(f"Error generating image: {e}") from e


# 单例实例
thirtytwo_nano_banana_provider: ThirtyTwoNanoBananaProvider = ThirtyTwoNanoBananaProvider()
