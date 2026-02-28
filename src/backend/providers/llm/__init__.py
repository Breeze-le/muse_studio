"""
LLM Provider 模块

提供多厂商 LLM 服务的统一抽象接口。

架构设计:
    采用抽象基类模式，所有 LLM 提供商继承自 BaseLLMProvider。
    这种设计使得添加新厂商变得简单，同时保持统一的调用接口。

扩展:
    要添加新的 LLM 提供商，请继承 BaseLLMProvider 并实现 generate() 方法。
    详见 docs/AI_PRD/architecture.md

支持的提供商:

    1. Zhipu AI (智谱)
       - 模型: glm-4.7-flash, glm-4.7, glm-4-plus, glm-z1-plus 等
       - 特性: 支持 thinking_enabled 深度思考模式
       - 推荐: glm-4.7-flash (免费额度较高)

    2. Gemini (Google)
       - 模型: gemini-2.5-flash, gemini-3-flash-preview, gemini-3.1-pro-preview 等
       - 特性: 支持 thinking_level 深度思考模式（仅 gemini-3 系列）
       - 推荐: gemini-2.5-flash (免费额度较高)

    3. 302.AI (模型聚合平台)
       - 平台: https://302.ai
       - 模型: 支持 Gemini、GPT、Claude、智谱等多种模型
       - 特性: OpenAI 兼容格式，统一 API 接入
       - 推荐: gemini-2.5-flash (通过 302.AI 调用)

模块结构:
    llm/
    ├── __init__.py     # 模块入口，导出所有 Provider
    ├── base.py         # BaseLLMProvider 抽象基类
    ├── zhipu.py        # ZhipuProvider 实现
    ├── gemini.py       # GeminiProvider 实现
    └── thirtytwo.py    # ThirtyTwoProvider 实现
"""

from .base import BaseLLMProvider
from .zhipu import ZhipuProvider, zhipu_provider
from .gemini import GeminiProvider, gemini_provider
from .thirtytwo import ThirtyTwoProvider, thirtytwo_provider

__all__ = [
    # 抽象基类
    "BaseLLMProvider",
    # Zhipu
    "ZhipuProvider",
    "zhipu_provider",
    # Gemini
    "GeminiProvider",
    "gemini_provider",
    # 302.AI
    "ThirtyTwoProvider",
    "thirtytwo_provider",
]
