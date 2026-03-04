"""Provider 参数元数据定义

定义参数规范数据结构，用于描述 generate 函数的参数属性。
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ParamSpec:
    """参数规范数据类

    用于描述 Provider generate 方法的参数元数据。

    Attributes:
        name: 参数名称
        type: 参数类型 (如 str, int, float, bool, list[str])
        exposed: 是否对外暴露（前端展示/API 接口）
        default: 默认值
        description: 参数描述
        choices: 可选值列表（枚举类型参数使用）
        required: 是否必填
    """

    name: str
    type: type
    exposed: bool
    default: Any = None
    description: str = ""
    choices: list[Any] | None = None
    required: bool = False


@dataclass(frozen=True)
class ProviderInfo:
    """Provider 信息数据类

    描述 Provider 的基本信息和参数规范。

    Attributes:
        provider_type: Provider 类型 (llm, image, video)
        vendor: 厂商名称 (如 zhipu, kling)
        model: 模型名称
        params: 参数规范列表
    """

    provider_type: str
    vendor: str
    model: str
    params: tuple[ParamSpec, ...] = field(default_factory=tuple)

    def get_exposed_params(self) -> list[ParamSpec]:
        """获取对外暴露的参数列表

        Returns:
            exposed=True 的参数列表
        """
        return [p for p in self.params if p.exposed]

    def get_param_dict(self) -> dict[str, ParamSpec]:
        """获取参数字典

        Returns:
            以参数名为 key 的参数字典
        """
        return {p.name: p for p in self.params}
