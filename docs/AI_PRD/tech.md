
## 核心模块设计

### 1. 配置管理 (`config.py`)

使用 `python-dotenv` 从 `.env` 文件加载配置。

```python
from src.backend.config import config

# 访问配置
api_key = config.ZHIPU_API_KEY
model = config.ZHIPU_MODEL_NAME
```

**支持的配置项**:

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `GEMINI_API_KEY` | Gemini API 密钥 | - |
| `GEMINI_MODEL_NAME` | Gemini 模型名 | `gemini-3.1-pro-preview` |
| `OPENAI_API_KEY` | OpenAI API 密钥 | - |
| `OPENAI_MODEL_NAME` | OpenAI 模型名 | `gpt-4o` |
| `ANTHROPIC_API_KEY` | Anthropic API 密钥 | - |
| `ANTHROPIC_MODEL_NAME` | Anthropic 模型名 | `claude-sonnet-4-20250514` |
| `ZHIPU_API_KEY` | 智谱 API 密钥 | - |
| `ZHIPU_MODEL_NAME` | 智谱模型名 | `glm-4.7` |

---

### 2. 日志系统 (`utils.py`)

统一的日志配置，支持控制台和文件双输出。

**特性**:
- 自动创建日志目录（项目根目录下的 `logs/`）
- 带时间戳的日志文件名
- 分级输出（控制台 INFO+，文件 DEBUG+）
- 防止重复添加 Handler

**使用方式**:

```python
from src.backend.utils import logger

# 各种日志等级
logger.debug("详细调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")
```

**日志格式**:
```
2026-02-27 22:17:46 - muse_studio - INFO - 这是一条日志
```

---

### 3. LLM Provider 架构

#### 3.1 设计模式

采用**抽象基类模式**，所有 LLM 提供商继承 `BaseLLMProvider`。

```
BaseLLMProvider (抽象基类)
    ├── generate() [抽象方法]
    └── is_available()
         │
         ├── ZhipuProvider (智谱 AI)
         ├── GeminiProvider (Google，待实现)
         ├── OpenAIProvider (OpenAI，待实现)
         └── AnthropicProvider (Anthropic，待实现)
```

#### 3.2 BaseLLMProvider (`base.py`)

所有 LLM 提供商的抽象基类。

**接口定义**:

```python
class BaseLLMProvider(ABC):
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.client = None

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本内容（必须实现）"""
        pass

    def is_available(self) -> bool:
        """检查客户端是否可用"""
        return self.client is not None
```

#### 3.3 ZhipuProvider (`zhipu.py`)

智谱 AI 的实现。

**特性**:
- 支持深度思考模式 (`thinking_enabled`)
- 自动错误处理和日志记录
- 支持自定义 `temperature`、`max_tokens`

**使用方式**:

```python
from src.backend.providers.llm import ZhipuProvider, zhipu_provider

# 方式 1: 直接使用单例
response = zhipu_provider.generate("用一句话解释量子计算")

# 方式 2: 创建新实例
provider = ZhipuProvider()
response = provider.generate(
    "1+1等于几？",
    thinking_enabled=True,
    temperature=0.7,
    max_tokens=1000
)
```

**参数说明**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | str | - | 输入提示词 |
| `thinking_enabled` | bool | False | 是否启用深度思考模式 |
| `temperature` | float | 1.0 | 随机性控制 (0.0-1.0) |
| `max_tokens` | int | 65536 | 最大输出 tokens |

---

### 4. 测试架构

#### 4.1 目录结构

```
tests/
├── conftest.py       # Pytest 全局配置
└── llm/              # LLM 测试
    └── test_zhipu.py # ZhipuProvider 测试
```

#### 4.2 运行测试

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest tests/llm/test_zhipu.py

# 详细输出
pytest -v

# 带覆盖率
pytest --cov=src/backend
```

#### 4.3 测试约定

- 需要真实 API 调用的测试使用 `@pytest.mark.skipif` 跳过
- 跳过条件：环境变量未配置或为默认占位符
- 测试文件命名：`test_<module>.py`
- 测试类命名：`Test<ClassName>`

---

## 扩展指南

### 添加新的 LLM 提供商

1. 在 `src/backend/providers/llm/` 下创建新文件，如 `gemini.py`

2. 继承 `BaseLLMProvider`：

```python
from .base import BaseLLMProvider
from src.backend.config import config
from src.backend.utils import logger

class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM 提供商"""

    def __init__(self):
        super().__init__(config.GEMINI_API_KEY, config.GEMINI_MODEL_NAME)
        # 初始化客户端...

    def generate(self, prompt: str, **kwargs) -> str:
        # 实现生成逻辑...
        pass

# 单例实例
gemini_provider: GeminiProvider = GeminiProvider()
```

3. 在 `__init__.py` 中导出：

```python
from .gemini import GeminiProvider, gemini_provider

__all__ = [
    # ...
    "GeminiProvider",
    "gemini_provider",
]
```

4. 在 `config.py` 中添加配置项

5. 在 `.env.example` 中添加配置示例

6. 在 `tests/llm/` 下添加测试文件

---

## 依赖管理

### 核心依赖 (`requirements.txt`)

| 包名 | 用途 |
|------|------|
| `google-genai` | Google Gemini API |
| `python-dotenv` | 环境变量管理 |
| `zhipuai` | 智谱 AI SDK |
| `socksio` | SOCKS 代理支持 |

### 开发依赖

| 包名 | 用途 |
|------|------|
| `pytest` | 测试框架 |
| `pytest-cov` | 覆盖率统计 |
| `pytest-asyncio` | 异步测试支持 |

---

## 开发工作流

### 1. 环境初始化

```bash
# 运行初始化脚本
./scripts/setup.sh
```

### 2. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env，填入真实的 API Keys
```

### 3. 运行测试

```bash
# 使用测试脚本
./scripts/test.sh

# 或直接使用 pytest
pytest -v
```

### 4. 查看日志

```bash
# 查看最新日志
tail -f logs/app_*.log
```

---

## 设计原则

1. **简单优先**: 不过度抽象，够用就好
2. **统一接口**: 所有 Provider 实现相同接口
3. **错误处理**: 统一的错误处理和日志记录
4. **配置驱动**: 通过环境变量控制行为
5. **测试友好**: 易于 mock 和测试
