"""GeminiProvider generate 函数测试

需要配置 GEMINI_API_KEY 环境变量才能运行。
"""

import os
import pytest

from src.backend.providers.llm.gemini import GeminiProvider
from src.backend.logger import logger


@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="需要配置 GEMINI_API_KEY"
)
class TestGeminiGenerate:
    """测试 generate 函数"""

    def test_generate_simple_response(self):
        """测试简单文本生成"""
        model_name = "gemini-2.5-flash"
        provider = GeminiProvider()
        provider.model_name = model_name
        prompt = "用一句话解释什么是量子计算"

        logger.info(f"[LLM INPUT] Model: {provider.model_name}, Prompt: {prompt}")
        response = provider.generate(prompt)
        logger.info(f"[LLM OUTPUT] Response: {response[:200]}..." if len(response) > 200 else f"[LLM OUTPUT] Response: {response}")

        assert response
        assert isinstance(response, str)
        assert len(response) > 10
        assert "Error" not in response

    def test_generate_with_thinking_level(self):
        """测试不同思考级别"""
        model_name = "gemini-2.5-flash"
        provider = GeminiProvider()
        provider.model_name = model_name
        prompt = "1+1等于几？"

        for level in ["low", "high"]:
            logger.info(f"[LLM INPUT] Model: {provider.model_name}, Prompt: {prompt}, Thinking: {level}")
            response = provider.generate(prompt, thinking_level=level)
            logger.info(f"[LLM OUTPUT] Response: {response[:200]}..." if len(response) > 200 else f"[LLM OUTPUT] Response: {response}")

            assert response
            assert isinstance(response, str)
