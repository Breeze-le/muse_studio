# Muse AI Studio

AI-powered creative studio for generating fashion outfits, canvas art, and multimedia content.

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
├── logs/                         # 日志目录
├── scripts/                      # 项目运行与运维脚本
│   ├── setup.sh                  # 初始化环境脚本
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
│   │   ├── services/             # 核心业务逻辑
│   │   │   ├── generation.py     # 调度 AI 生成（重点逻辑放这）
│   │   │   ├── outfit.py
│   │   │   └── canvas.py
│   │   └── providers/            # 外部 API 封装（个人项目的核心价值）
│   │       ├── llm.py            # LLM 提供商抽象基类 + 多厂商实现
│   │       ├── image_gen.py      # DALL·E / Flux 放一起
│   │       └── video_gen.py      # Runway / Kling 放一起
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
└── tests/                        # 测试（轻量，只测核心路径）
    ├── conftest.py               # 测试配置/夹具
    ├── test_providers.py         # 重点测 API 封装是否正常
    └── test_generation.py        # 重点测生成流程
```


### 已实现的厂商

| 厂商 | 类名 | 状态 |
|------|------|------|
| 智谱 AI | `ZhipuProvider` | ✅ 已实现 |
| Google Gemini | `GeminiProvider` | 🚧 预留 |
| OpenAI | `OpenAIProvider` | 🚧 预留 |
| Anthropic | `AnthropicProvider` | 🚧 预留 |



## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入 API Keys
```

### 3. 运行测试

```bash
python tests/manual_test_llm.py
```

### 4. 启动服务

```bash
./scripts/setup.sh    # 初始化环境
./scripts/restart.sh  # 启动服务
```

## 开发规范

- **代码风格**: 遵循 PEP 8
- **提交规范**: 使用 Conventional Commits
- **测试覆盖**: 核心路径 80%+ 覆盖率
- **文档**: 代码变更同步更新 README

## License

MIT
