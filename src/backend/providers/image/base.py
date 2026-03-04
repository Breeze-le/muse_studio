"""
Image Provider 抽象基类

定义所有 Image 提供商必须实现的接口。
"""

from abc import ABC, abstractmethod
from typing import Any

from ..param_spec import ParamSpec


class BaseImageProvider(ABC):
    """Image 提供商抽象基类

    所有 Image 提供商必须继承此类并实现 generate() 方法。
    这种设计模式允许在不修改现有代码的情况下添加新的 Image 服务。

    Attributes:
        api_key: API 密钥
        model_name: 模型名称
        client: 底层 API 客户端实例
        GENERATE_PARAMS: generate 方法参数规范（子类应覆盖）

    示例:
        >>> class CustomProvider(BaseImageProvider):
        ...     def generate(self, prompt: str, **kwargs) -> bytes:
        ...         return b"image_data"
    """

    # 子类应覆盖此属性定义参数规范
    GENERATE_PARAMS: tuple[ParamSpec, ...] = ()

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

    @classmethod
    def get_exposed_params(cls) -> list[ParamSpec]:
        """获取对外暴露的参数列表

        返回 exposed=True 的参数，用于前端展示和 API 参数过滤。

        Returns:
            对外暴露的参数规范列表
        """
        return [p for p in cls.GENERATE_PARAMS if p.exposed]

    @classmethod
    def get_param_dict(cls) -> dict[str, ParamSpec]:
        """获取参数字典

        Returns:
            以参数名为 key 的参数字典
        """
        return {p.name: p for p in cls.GENERATE_PARAMS}

    @classmethod
    def get_provider_info(cls) -> dict[str, Any]:
        """获取 Provider 信息

        Returns:
            包含 provider 类型、参数规范等信息的字典
        """
        return {
            "provider_type": "image",
            "params": [
                {
                    "name": p.name,
                    "type": p.type.__name__ if hasattr(p.type, "__name__") else str(p.type),
                    "exposed": p.exposed,
                    "default": p.default,
                    "description": p.description,
                    "choices": p.choices,
                    "required": p.required,
                }
                for p in cls.GENERATE_PARAMS
            ],
            "exposed_params": [
                {
                    "name": p.name,
                    "type": p.type.__name__ if hasattr(p.type, "__name__") else str(p.type),
                    "default": p.default,
                    "description": p.description,
                    "choices": p.choices,
                    "required": p.required,
                }
                for p in cls.get_exposed_params()
            ],
        }
