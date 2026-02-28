"""302.AI LLM 提供商

302.AI 是一个 AI 模型聚合平台，提供 OpenAI 兼容格式的统一 API。
支持 Gemini、GPT、Claude、智谱等多种模型。

官方文档: https://302ai.apifox.cn/api-147522041
价格: https://302.ai/price

可用模型列表（Gemini 系列）:
    - gemini-2.5-flash                    # 快速响应版（推荐）
    - gemini-2.5-pro                      # 专业版
    - gemini-3-pro-preview                # 第三代专业版预览
    - gemini-2.5-flash-preview-05-20      # Flash 预览版
    - gemini-2.5-flash-lite-preview-06-17 # Flash 轻量版
    - gemini-2.5-pro-preview-06-05        # Pro 预览版
    - gemini-2.5-pro-preview-06-05-thinking # Pro 预览版（展示思考）

更多模型请参考: https://doc.302.ai/147522041e0
"""

from src.backend.config import config
from src.backend.logger import logger
from .base import BaseLLMProvider


class ThirtyTwoProvider(BaseLLMProvider):
    """302.AI LLM 提供商

    302.AI 是一个 AI 模型聚合平台，提供 OpenAI 兼容格式的统一 API。
    支持多种主流 AI 模型，包括 Gemini、GPT、Claude、智谱等。

    特性:
        - OpenAI 兼容格式
        - 支持流式输出
        - 自动错误处理和日志记录

    环境变量:
        THIRTYTWO_API_KEY: 302.AI API 密钥（必需）
        THIRTYTWO_MODEL_NAME: 模型名称（默认: gemini-2.5-flash）

    示例:
        >>> provider = ThirtyTwoProvider()
        >>> if provider.is_available():
        ...     response = provider.generate("用一句话解释量子计算")
    """

    def __init__(self):
        super().__init__(config.THIRTYTWO_API_KEY, config.THIRTYTWO_MODEL_NAME)

        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.302.ai/v1"
                )
                logger.info(f"ThirtyTwoProvider initialized with model: {self.model_name}")
            except ImportError:
                logger.debug("openai package is not installed. Run: pip install openai")
            except Exception as e:
                logger.debug(f"Failed to initialize ThirtyTwo client: {e}")
                self.client = None

    def generate(
        self,
        prompt: str,
        temperature: float = 1.0,
        max_tokens: int = 65536,
        stream: bool = False,
    ) -> str:
        """使用配置的 302.AI 模型生成内容

        Args:
            prompt: 输入提示词
            temperature: 控制输出的随机性 (0.0-2.0)
            max_tokens: 最大输出 tokens 数
            stream: 是否使用流式输出

        Returns:
            str: 生成的文本内容，如果出错则返回错误信息字符串
        """
        if not self.client:
            logger.warning("ThirtyTwoProvider client not available - check THIRTYTWO_API_KEY configuration")
            return "Error: LLM configuration missing."

        try:
            logger.info(f"Generating content for prompt: {prompt[:50]}...")

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )

            if stream:
                # 流式输出处理
                content = ""
                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content += chunk.choices[0].delta.content
                logger.info(f"Response (stream): {content[:200]}...")
                return content
            else:
                # 非流式输出
                if response.choices:
                    content = response.choices[0].message.content
                    logger.info(f"Response: {content[:200]}...")
                    return content if content else ""
                else:
                    logger.warning("Empty response from ThirtyTwo.AI")
                    return ""

        except Exception as e:
            logger.error(f"Error during generation: {e}")
            return f"Error generating content: {str(e)}"


# 单例实例
thirtytwo_provider: ThirtyTwoProvider = ThirtyTwoProvider()
