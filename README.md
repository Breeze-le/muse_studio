# Muse AI Studio

AI-powered creative studio for generating fashion outfits, canvas art, and multimedia content.

> **当前状态**: 基础脚手架搭建完成，正在添加外部模型 API 供应商。前端/后端业务逻辑尚未实现。

## Project Structure

```
muse_studio/
├── .env                          # API Keys、配置（直接用，别过度抽象）
├── .env.example                  # 配置示例文件
├── .gitignore                    # Git 忽略规则
├── README.md                     # 项目说明文档
├── requirements.txt              # Python 依赖
├── package.json                  # 前端依赖
├── docs/                         # 所有文档合并到一处
│   ├── PRD/                      # 产品需求(给人看)
│   └── AI_PRD/                   # AI 实现PRD(给 AI 看)
│       └── provider_sop.md       # 模型/供应商添加标准操作流程
├── logs/                         # 日志目录（所有日志输出至此）
├── scripts/                      # 项目运行与运维脚本
│   ├── setup.sh                  # 环境构建脚本（创建 venv + 安装依赖）
│   ├── restart.sh                # 重启服务脚本
│   └── test.sh                   # 一键运行测试脚本
├── src/                          # 源代码主目录
│   ├── backend/                  # 后端（FastAPI）
│   │   ├── main.py               # 入口 + 路由全在这，够用再拆
│   │   ├── config.py             # 读 .env，暴露配置常量
│   │   ├── database.py           # DB 连接（PostgreSQL 优先，简单够用）
│   │   ├── models.py             # 所有 ORM 模型放一起（早期不用拆）
│   │   ├── schemas.py            # 所有 Pydantic Schema 放一起
│   │   ├── utils.py              # 日志、异常、工具函数全在一起
│   │   ├── services/             # 核心业务逻辑（待实现）
│   │   │   ├── generation.py     # 调度 AI 生成（重点逻辑放这）
│   │   │   ├── outfit.py
│   │   │   └── canvas.py
│   │   └── providers/            # 外部 API 封装（正在开发中）
│   │       ├── llm/              # LLM 提供商
│   │       │   ├── base.py       # BaseLLMProvider 抽象基类
│   │       │   ├── zhipu.py      # 智谱 AI 实现
│   │       │   ├── gemini.py     # Google Gemini 实现
│   │       │   └── thirtytwo.py  # 302.AI 模型聚合平台实现
│   │       ├── image/            # 图像生成提供商
│   │       │   ├── base.py       # BaseImageProvider 抽象基类
│   │       │   └── thirtytwo.py  # 302.AI 图像生成实现
│   │       └── video/            # 视频生成提供商
│   │           ├── base.py       # BaseVideoProvider 抽象基类
│   │           └── thirtytwo_kling.py  # 302.AI Kling 视频生成实现
│   └── frontend/                 # 前端（React + TS / 或直接用 HTML）
│       ├── index.html
│       ├── vite.config.ts
│       └── src/
│           ├── main.tsx
│           ├── App.tsx
│           ├── api.ts            # 所有接口请求统一放一个文件
│           ├── store.ts          # 状态管理（Zustand，一个文件够）
│           ├── types.ts          # 所有类型定义放一起
│           ├── components/       # 组件（扁平放，别过早分 ui/business）
│           │   ├── OutfitCard.tsx
│           │   ├── CanvasEditor.tsx
│           │   └── GenerationPanel.tsx
│           ├── pages/
│           │   ├── Home.tsx
│           │   ├── Canvas.tsx
│           │   └── Generation.tsx
│           └── hooks/
│               └── useGeneration.ts  # 轮询生成状态（值得单独一个 hook）
└── tests/                        # 测试（新增代码必须添加测试）
    ├── conftest.py               # 测试配置/夹具
    ├── llm/                      # LLM 提供商测试
    │   ├── test_zhipu.py         # 智谱 AI 测试
    │   ├── test_gemini.py        # Gemini 测试
    │   └── test_thirtytwo.py     # 302.AI 测试
    ├── image/                    # 图像提供商测试
    │   └── test_thirtytwo.py     # 302.AI 图像测试
    └── video/                    # 视频提供商测试
        └── test_thirtytwo_kling.py  # 302.AI Kling 视频测试
```


### 已实现的厂商

#### LLM 提供商

| 厂商 | 类名 | 状态 | 推荐模型 |
|------|------|------|----------|
| 智谱 AI | `ZhipuProvider` | ✅ 已实现 | `glm-4.7-flash` |
| Google Gemini | `GeminiProvider` | ✅ 已实现 | `gemini-2.5-flash` |
| 302.AI | `ThirtyTwoProvider` | ✅ 已实现 | `gemini-2.5-flash` |
| OpenAI | `OpenAIProvider` | 🚧 待实现 | - |
| Anthropic | `AnthropicProvider` | 🚧 待实现 | - |

#### 图像生成提供商

| 厂商 | 类名 | 状态 | 推荐模型 |
|------|------|------|----------|
| 302.AI | `ThirtyTwoImageProvider` | ✅ 已实现 | `google/nano-banana-2` / `doubao-seedream-5-0-260128` |

#### 视频生成提供商

| 厂商 | 类名 | 状态 | 推荐模型 |
|------|------|------|----------|
| 302.AI Kling | `ThirtyTwoKlingProvider` | ✅ 已实现 | `kling-v-1-5-260121` / `kling-v2-5-turbo` |

---

## 快速开始

### 1. 环境构建

```bash
./scripts/setup.sh    # 创建虚拟环境并安装依赖
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入对应厂商的 API Keys
```

### 3. 运行测试

```bash
# 运行全部测试
./scripts/test.sh

# 运行指定类型测试
./scripts/test.sh tests/llm/        # 仅 LLM 测试
./scripts/test.sh tests/image/      # 仅图像测试
./scripts/test.sh tests/video/      # 仅视频测试
./scripts/test.sh tests/llm/test_zhipu.py  # 指定文件
```

### 4. 查看日志

```bash
# 测试日志（带时间戳）
ls -lt logs/test_*.log | head -1 | xargs tail -f

# 实时监控最新日志
tail -f logs/test_*.log
```

### 5. 启动服务

```bash
./scripts/restart.sh  # 重启后端服务
```

## 开发规范

### 添加新供应商

添加新的 AI 模型/供应商请遵循 `docs/AI_PRD/provider_sop.md` 中的标准流程：

1. 创建 Provider 文件：`src/backend/providers/<type>/<vendor>.py`
2. 更新模块导出：`__init__.py`
3. 添加配置项：`config.py` + `.env.example`
4. 创建测试：`tests/<type>/test_<vendor>.py`
5. 运行测试验证：`./scripts/test.sh`

### 通用规范

- **代码风格**: 遵循 PEP 8
- **提交规范**: 使用 Conventional Commits（feat/fix/refactor/docs/test）
- **测试覆盖**: 新增代码必须添加测试，核心路径 80%+ 覆盖率
- **日志输出**: 所有日志输出到 `logs/` 目录
- **文档**: 代码变更同步更新 README

## License

MIT
