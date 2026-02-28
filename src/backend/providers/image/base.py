"""
Image Provider 抽象基类

定义所有 Image 提供商必须实现的接口。
"""

from abc import ABC, abstractmethod


class BaseImageProvider(ABC):
    """Image 提供商抽象基类

    所有 Image 提供商必须继承此类并实现 generate() 方法。
    这种设计模式允许在不修改现有代码的情况下添加新的 Image 服务。

    Attributes:
        api_key: API 密钥
        model_name: 模型名称
        client: 底层 API 客户端实例

    示例:
        >>> class CustomProvider(BaseImageProvider):
        ...     def generate(self, prompt: str, **kwargs) -> bytes:
        ...         return b"image_data"
    """

    def __init__(self, api_key: str, model_name: str):
        """初始化 Image 提供商

        Args:
            api_key: API 密钥
            model_name: 模型名称
        """
        self.api_key = api_key
        self.model_name = model_name
        self.client = None

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> bytes:
        """生成图片内容（抽象方法，必须由子类实现）

        Args:
            prompt: 图片描述提示词（必填）
            **kwargs: 厂商特定参数（如 size, n, quality, style 等）

        Returns:
            生成的图片数据（bytes 格式）

        Raises:
            NotImplementedError: 如果子类未实现此方法
        """
        pass

    def is_available(self) -> bool:
        """检查客户端是否可用

        Returns:
            bool: 客户端是否已成功初始化
        """
        return self.client is not None
