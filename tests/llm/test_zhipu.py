"""ZhipuProvider generate 函数测试

需要配置 ZHIPU_API_KEY 环境变量才能运行。
"""

import os
import pytest

from src.backend.providers.llm.zhipu import ZhipuProvider


@pytest.mark.skipif(
    not os.getenv("ZHIPU_API_KEY") or os.getenv("ZHIPU_API_KEY") == "your_zhipu_api_key_here",
    reason="需要配置有效的 ZHIPU_API_KEY"
)
class TestZhipuGenerate:
    """测试 generate 函数"""

    def test_generate_simple_response(self):
        """测试简单文本生成"""
        provider = ZhipuProvider()
        response = provider.generate("用一句话解释什么是量子计算")

        assert response
        assert isinstance(response, str)
        assert len(response) > 10
        assert "Error" not in response

    def test_generate_with_thinking_mode(self):
        """测试深度思考模式"""
        provider = ZhipuProvider()
        response = provider.generate("1+1等于几？", thinking_enabled=True)

        assert response
        assert isinstance(response, str)
        assert "Error" not in response
