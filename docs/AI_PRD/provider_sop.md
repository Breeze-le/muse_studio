# 模型/供应商添加 SOP

向 Muse AI Studio 添加新 AI 模型或供应商的标准操作流程。

---

## 目录

- [1. 架构与命名](#1-架构与命名)
- [2. 添加供应商](#2-添加供应商)
- [3. 测试验证](#3-测试验证)
- [4. 检查清单](#4-检查清单)
- [5. 已实现供应商](#5-已实现供应商)

---

## 1. 架构与命名

### 目录结构

```
src/backend/providers/
├── llm/               # LLM 供应商
│   ├── base.py        # BaseLLMProvider (抽象基类)
│   └── *.py           # 各 LLM 供应商实现
└── image/             # 图像生成供应商
    ├── base.py        # BaseImageProvider (抽象基类)
    └── *.py           # 各图像供应商实现
```

### 命名约定

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| 模块文件 | 小写下划线 | `thirtytwo.py` |
| Provider 类 | `*Provider` | `ThirtyTwoProvider` |
| 单例实例 | 小写下划线 | `thirtytwo_provider` |
| 配置项 | 大写下划线 | `THIRTYTWO_API_KEY` |
| 测试文件 | `test_*.py` | `test_thirtytwo.py` |

### 前置信息收集

- 官方文档链接
- API 认证方式（API Key / Bearer Token）
- 请求/响应格式（OpenAI 兼容 / 原生）
- 可用模型列表及推荐模型
- 特殊参数（temperature / max_tokens / thinking_level 等）
- SDK 包名（如使用官方 SDK）

---

## 2. 添加供应商

### 步骤概览

```
1. 创建 Provider 文件     2. 更新模块导出
src/backend/providers/      __init__.py
  llm/<vendor>.py           or image/<vendor>.py

         ↓                        ↓
3. 添加配置项               4. 创建测试
config.py + .env.example    tests/<type>/test_<vendor>.py
```

### 2.1 LLM Provider 模板

**文件**: `src/backend/providers/llm/<vendor>.py`

```python
"""<供应商名称> LLM 提供商

官方文档: <文档链接>
可用模型: <model-1>(推荐), <model-2>, ...
"""

from src.backend.config import config
from src.backend.logger import logger
from .base import BaseLLMProvider


class <Vendor>Provider(BaseLLMProvider):
    """<供应商名称> LLM 提供商

    环境变量:
        <VENDOR>_API_KEY: API 密钥（必需）
        <VENDOR>_MODEL_NAME: 模型名称（默认: <default-model>）
    """

    def __init__(self):
        super().__init__(config.<VENDOR>_API_KEY, config.<VENDOR>_MODEL_NAME)
        if self.api_key:
            try:
                self.client = <ClientClass>(api_key=self.api_key, ...)
                logger.info(f"<Vendor>Provider initialized: {self.model_name}")
            except Exception as e:
                logger.debug(f"Failed to init <vendor> client: {e}")
                self.client = None

    def generate(self, prompt: str, temperature: float = 1.0,
                 max_tokens: int = 65536, stream: bool = False, **kwargs) -> str:
        if not self.client:
            return "Error: LLM configuration missing."
        try:
            response = self.client.<method>(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature, max_tokens=max_tokens, stream=stream,
            )
            if stream:
                return "".join(c.choices[0].delta.content or "" for c in response if c.choices)
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return f"Error: {str(e)}"


<vendor>_provider: <Vendor>Provider = <Vendor>Provider()
```

### 2.2 添加配置

**`src/backend/config.py`**:
```python
<VENDOR>_API_KEY = os.getenv("<VENDOR>_API_KEY")
<VENDOR>_MODEL_NAME = os.getenv("<VENDOR>_MODEL_NAME", "<default-model>")
```

**`.env.example`**:
```bash
# <供应商> API
<VENDOR>_API_KEY=your_<vendor>_api_key_here
<VENDOR>_MODEL_NAME=<default-model>
```

---

## 3. 测试验证

### 测试模板

**LLM**: `tests/llm/test_<vendor>.py`
```python
import os
import pytest
from src.backend.providers.llm.<vendor> import <Vendor>Provider

@pytest.mark.skipif(not os.getenv("<VENDOR>_API_KEY"), reason="需要 API Key")
class Test<Vendor>Generate:
    def test_generate_simple_response(self):
        response = <Vendor>Provider().generate("用一句话解释量子计算")
        assert response and len(response) > 10 and "Error" not in response
```

**Image**: `tests/image/test_<vendor>.py`
```python
import os
import pytest
from src.backend.providers.image.<vendor> import <Vendor>ImageProvider

@pytest.mark.skipif(not os.getenv("<VENDOR>_API_KEY"), reason="需要 API Key")
class Test<Vendor>ImageGenerate:
    def test_generate_simple_image(self):
        result = <Vendor>ImageProvider().generate("一只在月球上的猫")
        assert len(result.image_data) > 1000
```

### 运行测试
```bash
PYTHONPATH=/Users/saymefat/Desktop/muse_studio pytest tests/llm/test_<vendor>.py -v
```

---

## 4. 检查清单

### 通用步骤
- [ ] 创建 Provider 文件 `src/backend/providers/<type>/<vendor>.py`
- [ ] 更新模块导出 `__init__.py`
- [ ] 添加配置项到 `config.py` 和 `.env.example`
- [ ] 创建测试文件 `tests/<type>/test_<vendor>.py`
- [ ] 运行测试验证功能
- [ ] 更新本文档"已实现供应商"章节