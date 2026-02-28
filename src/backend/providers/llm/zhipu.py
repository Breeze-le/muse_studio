"""
智谱 AI LLM 提供商

支持 GLM-4.7、GLM-4 Plus、GLM-Z1 等系列模型。

可用 LLM 模型列表:
    - glm-4.7-flash          # 快速响应版（推荐）
    - glm-4.7-flashx         # 更快速的增强版
    - glm-4.7                # 标准版，支持 thinking
    - glm-4.7-air            # 轻量版
    - glm-4-plus             # 增强版，支持 thinking
    - glm-4-0520             # 稳定版本
    - glm-4-flash            # Flash 版本
    - glm-4-airx             # 轻量增强版
    - glm-z1-plus            # Z1 增强版
    - glm-z1-air             # Z1 轻量版
    - glm-z1-preview         # Z1 预览版

注意:
    - thinking_enabled 参数支持: glm-4.7, glm-4-plus 等专业版
    - 免费套餐推荐: glm-4.7-flash
"""

from src.backend.config import config
from src.backend.logger import logger
from .base import BaseLLMProvider


class ZhipuProvider(BaseLLMProvider):
    """智谱 AI LLM 提供商

    支持 GLM-4.7、GLM-4 Plus、GLM-Z1 等系列模型。

    特性:
        - 支持深度思考模式 (thinking_enabled)
        - 使用 zhipuai SDK
        - 自动错误处理和日志记录

    环境变量:
        ZHIPU_API_KEY: 智谱 API 密钥（必需）
        ZHIPU_MODEL_NAME: 模型名称（默认: glm-4.7-flash）

    示例:
        >>> provider = ZhipuProvider()
        >>> if provider.is_available():
        ...     response = provider.generate("用一句话解释量子计算")
    """

    def __init__(self):
        super().__init__(config.ZHIPU_API_KEY, config.ZHIPU_MODEL_NAME)

        if self.api_key:
            try:
                from zhipuai import ZhipuAI
                self.client = ZhipuAI(api_key=self.api_key)
                logger.info(f"ZhipuProvider initialized with model: {self.model_name}")
            except ImportError:
                logger.debug("zhipuai package is not installed. Run: pip install zhipuai")
            except Exception as e:
                logger.debug(f"Failed to initialize Zhipu client: {e}")
                self.client = None

    def generate(
        self,
        prompt: str,
        thinking_enabled: bool = False,
        temperature: float = 1.0,
        max_tokens: int = 65536,
    ) -> str:
        """使用配置的智谱模型生成内容

        Args:
            prompt: 输入提示词
            thinking_enabled: 是否启用深度思考模式
            temperature: 控制输出的随机性 (0.0-1.0)
            max_tokens: 最大输出 tokens 数

        Returns:
            str: 生成的文本内容，如果出错则返回错误信息字符串

        Note:
            thinking_enabled 是智谱特有的参数，启用后模型会进行深度思考。
        """
        if not self.client:
            logger.warning("ZhipuProvider client not available - check ZHIPU_API_KEY configuration")
            return "Error: LLM configuration missing."

        try:
            logger.info(f"Generating content for prompt: {prompt[:50]}...")

            # 构建请求参数
            request_params = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature,
            }

            # 启用深度思考模式
            if thinking_enabled:
                request_params["thinking"] = {"type": "enabled"}

            response = self.client.chat.completions.create(**request_params)

            if response.choices:
                content = response.choices[0].message.content
                # 处理可能的 reasoning_content（思考过程）
                if hasattr(response.choices[0].message, 'reasoning_content') and response.choices[0].message.reasoning_content:
                    logger.debug(f"Reasoning: {response.choices[0].message.reasoning_content[:100]}...")
                if content:
                    logger.info(f"Response: {content[:200]}...")
                return content if content else ""
            else:
                logger.warning("Empty response from Zhipu.")
                return ""

        except Exception as e:
            logger.error(f"Error during generation: {e}")
            return f"Error generating content: {str(e)}"


# 单例实例
zhipu_provider: ZhipuProvider = ZhipuProvider()
