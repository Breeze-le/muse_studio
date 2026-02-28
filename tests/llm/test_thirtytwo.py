"""ThirtyTwoProvider generate 函数测试

需要配置 THIRTYTWO_API_KEY 环境变量才能运行。
302.AI 官方文档: https://302ai.apifox.cn/api-147522041
"""

import os
import pytest

from src.backend.providers.llm.thirtytwo import ThirtyTwoProvider
from src.backend.logger import logger


@pytest.mark.skipif(
    not os.getenv("THIRTYTWO_API_KEY") or os.getenv("THIRTYTWO_API_KEY") == "your_thirtytwo_api_key_here",
    reason="需要配置有效的 THIRTYTWO_API_KEY"
)
class TestThirtyTwoGenerate:
    """测试 generate 函数"""

    def test_generate_simple_response(self):
        """测试简单文本生成"""
        provider = ThirtyTwoProvider()
        prompt = "用一句话解释什么是量子计算"

        logger.info(f"[LLM INPUT] Model: {provider.model_name}, Prompt: {prompt}")
        response = provider.generate(prompt)
        logger.info(f"[LLM OUTPUT] Response: {response[:200]}..." if len(response) > 200 else f"[LLM OUTPUT] Response: {response}")

        assert response
        assert isinstance(response, str)
        assert len(response) > 10
        assert "Error" not in response


    def test_generate_stream(self):
        """测试流式输出"""
        provider = ThirtyTwoProvider()
        prompt = "用三句话介绍人工智能"

        logger.info(f"[LLM INPUT] Model: {provider.model_name}, Prompt: {prompt}, Stream: True")
        response = provider.generate(prompt, stream=True)
        logger.info(f"[LLM OUTPUT] Response: {response[:200]}..." if len(response) > 200 else f"[LLM OUTPUT] Response: {response}")

        assert response
        assert isinstance(response, str)
        assert len(response) > 10
        assert "Error" not in response

