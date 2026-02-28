# 模型/供应商添加 SOP

向 Muse AI Studio 添加新 AI 模型或供应商的标准操作流程。

---

## 目录

- [1. 架构与命名](#1-架构与命名)
- [2. 添加供应商](#2-添加供应商)
- [3. 依赖管理](#3-依赖管理)
- [4. 测试验证](#4-测试验证)
- [5. 检查清单](#5-检查清单)

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
- **SDK 包名及版本**（如使用官方 SDK）
- **测试所需额外依赖**（如 pytest 插件、mock 工具等）

---

## 2. 添加供应商

### 步骤概览

```
1. 创建 Provider 文件     2. 更新模块导出
src/backend/providers/      __init__.py
  llm/<vendor>.py           or image/<vendor>.py

         ↓                        ↓
3. 添加配置项               4. 管理依赖
config.py + .env.example    requirements.txt
                              + scripts/
         ↓                        ↓
5. 创建测试               6. 运行验证
tests/<type>/test_<vendor>.py  ./scripts/test.sh
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

## 3. 依赖管理

> **重要**: 每添加新供应商时，必须同步更新依赖配置文件。

### 3.1 添加生产依赖

**文件**: `requirements.txt`

```
# 在文件末尾添加新依赖，格式：
<package-name>==<version>  # <供应商> SDK
```

**示例**:
```
google-genai==1.0.0        # Google Gemini SDK
zhipuai==2.1.0             # 智谱 AI SDK
```

### 3.2 添加测试依赖

**文件**: `scripts/test.sh` 中的 `pip install` 行（如需测试专用依赖）

```bash
# 在检查 pytest 安装部分添加测试专用依赖
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}pytest 未安装，正在安装...${NC}"
    pip install pytest pytest-cov <test-package> -q
fi
```

### 3.3 安装新依赖

```bash
# 激活虚拟环境后运行
source .venv/bin/activate
pip install -r requirements.txt
```

或使用 setup 脚本：
```bash
./scripts/setup.sh
```

---

## 4. 测试验证

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

## 5. 检查清单

### 通用步骤
- [ ] 创建 Provider 文件 `src/backend/providers/<type>/<vendor>.py`
- [ ] 更新模块导出 `__init__.py`
- [ ] 添加配置项到 `config.py` 和 `.env.example`
- [ ] **添加依赖包到 `requirements.txt`**
- [ ] **如需测试专用依赖，更新 `scripts/test.sh`**
- [ ] 运行 `pip install -r requirements.txt` 安装新依赖
- [ ] 创建测试文件 `tests/<type>/test_<vendor>.py`
- [ ] 运行 `./scripts/test.sh` 验证功能
- [ ] 更新本文档"已实现供应商"章节（如有）

### 依赖管理检查项
- [ ] 记录供应商 SDK 包名和版本
- [ ] 记录测试所需额外依赖
- [ ] 更新 `requirements.txt`
- [ ] 更新 `scripts/test.sh`（如需）
- [ ] 验证依赖安装成功
- [ ] 测试无 import 错误