"""
LLM Provider 模块

提供多厂商 LLM 服务的统一抽象接口。

架构设计:
    采用抽象基类模式，所有 LLM 提供商继承自 BaseLLMProvider。
    这种设计使得添加新厂商变得简单，同时保持统一的调用接口。

扩展:
    要添加新的 LLM 提供商，请继承 BaseLLMProvider 并实现 generate() 方法。
    详见 docs/AI_PRD/architecture.md

模块结构:
    llm/
    ├── __init__.py     # 模块入口，导出所有 Provider
    ├── base.py         # BaseLLMProvider 抽象基类
    └── zhipu.py        # ZhipuProvider 实现
"""

from .base import BaseLLMProvider
from .zhipu import ZhipuProvider, zhipu_provider

__all__ = [
    # 抽象基类
    "BaseLLMProvider",
    # Zhipu
    "ZhipuProvider",
    "zhipu_provider",
]
