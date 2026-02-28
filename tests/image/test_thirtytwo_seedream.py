"""ThirtyTwoSeedreamProvider generate 函数测试

需要配置 THIRTYTWO_DOUBAO_API_KEY 或 THIRTYTWO_API_KEY 环境变量才能运行。
"""

import os
from datetime import datetime
from pathlib import Path

import pytest

from src.backend.providers.image.thirtytwo_seedream import ThirtyTwoSeedreamProvider
from src.backend.logger import logger

# 输出目录
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_image(image_data: bytes, prefix: str) -> Path:
    """保存图片到输出目录

    Args:
        image_data: 图片二进制数据
        prefix: 文件名前缀

    Returns:
        保存的文件路径
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.png"
    filepath = OUTPUT_DIR / filename

    with open(filepath, "wb") as f:
        f.write(image_data)

    logger.info(f"[IMAGE SAVED] {filepath}")
    return filepath


@pytest.mark.skipif(
    not (os.getenv("THIRTYTWO_DOUBAO_API_KEY") or os.getenv("THIRTYTWO_API_KEY")),
    reason="需要配置 THIRTYTWO_DOUBAO_API_KEY 或 THIRTYTWO_API_KEY"
)
class TestThirtyTwoSeedreamGenerate:
    """测试 Seedream generate 函数"""

    def test_generate_text_to_image_default_params(self):
        """测试文生图：仅使用提示词，其他参数使用默认值"""
        provider = ThirtyTwoSeedreamProvider()
        prompt = "一只可爱的橘猫坐在窗台上，阳光洒在它身上，数字艺术风格"

        logger.info(f"[IMAGE INPUT] Model: {provider.model_name}, Prompt: {prompt}")
        image_data = provider.generate(prompt)
        logger.info(f"[IMAGE OUTPUT] Generated image size: {len(image_data)} bytes")

        # 保存图片
        save_image(image_data, "seedream_text_to_image")

        assert image_data
        assert isinstance(image_data, bytes)
        assert len(image_data) > 1000  # 图片数据应该大于 1KB

    def test_generate_with_single_image(self):
        """测试图生图：提示词 + 单张图片，其他参数使用默认值"""
        provider = ThirtyTwoSeedreamProvider()
        prompt = "变成卡通风格"
        # 使用公开的测试图片 URL
        image_url = "https://common-oss-cdn.tiangong.tech/application-data/prod/2025-12-16/tiangong_ea8ac72e6cf142669421d85ab9bdcc9.png"

        logger.info(f"[IMAGE INPUT] Model: {provider.model_name}, Prompt: {prompt}, Image: {image_url}")
        image_data = provider.generate(prompt, image=image_url)
        logger.info(f"[IMAGE OUTPUT] Generated image size: {len(image_data)} bytes")

        # 保存图片
        save_image(image_data, "seedream_single_image_to_image")

        assert image_data
        assert isinstance(image_data, bytes)
        assert len(image_data) > 1000  # 图片数据应该大于 1KB

    def test_generate_with_multiple_images(self):
        """测试多图融合：提示词 + 多张图片，其他参数使用默认值"""
        provider = ThirtyTwoSeedreamProvider()
        prompt = "将图1的服装换为图2的服装"
        # 使用多张公开的测试图片 URL
        image_urls = [
            "https://common-oss-cdn.tiangong.tech/application-data/prod/2025-12-16/tiangong_ea8ac72e6cf142669421d85ab9bdcc9.png",
            "https://jv-comfyui-image.tiangong.tech/dify_upload/dify_upload_1767515452_233867f6-ec5d-474d-8cb5-e426c0b62767.png"
        ]

        logger.info(f"[IMAGE INPUT] Model: {provider.model_name}, Prompt: {prompt}, Images count: {len(image_urls)}")
        image_data = provider.generate(prompt, image=image_urls)
        logger.info(f"[IMAGE OUTPUT] Generated image size: {len(image_data)} bytes")

        # 保存图片
        save_image(image_data, "seedream_multiple_images")

        assert image_data
        assert isinstance(image_data, bytes)
        assert len(image_data) > 1000  # 图片数据应该大于 1KB

