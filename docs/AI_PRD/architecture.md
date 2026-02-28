# Muse AI Studio 架构设计

## 项目概览

Muse AI Studio 是一个 AI 内容生成平台，支持多厂商 LLM、图像生成、视频生成服务。

**技术栈**: Python 3.12+ / FastAPI / PostgreSQL / Pytest

---

## 项目结构

```
muse_studio/
├── .env                          # API Keys、配置（不提交到 Git）
├── .env.example                  # 配置示例文件
├── .gitignore                    # Git 忽略规则
├── README.md                     # 项目说明文档
├── requirements.txt              # Python 依赖
├── docs/                         # 文档目录
│   ├── PRD/                      # 产品需求文档
│   └── AI_PRD/                   # AI 实现指南
│       └── architecture.md       # 本文档
├── logs/                         # 日志输出目录
│   └── app_YYYYMMDD_HHMMSS.log   # 带时间戳的日志文件
├── scripts/                      # 项目运行与运维脚本
│   ├── setup.sh                  # 初始化环境脚本
│   ├── test.sh                   # 运行测试脚本
├── src/                          # 源代码主目录
│   └── backend/                  # 后端代码
│       ├── main.py               # FastAPI 入口（待实现）
│       ├── config.py             # 配置管理（读取 .env）
│       ├── database.py           # 数据库连接（待实现）
│       ├── models.py             # ORM 模型（待实现）
│       ├── schemas.py            # Pydantic Schema（待实现）
│       ├── utils.py              # 日志、工具函数
│       ├── services/             # 核心业务逻辑
│       │   ├── generation.py     # AI 生成调度服务
│       │   ├── outfit.py         # Outfit 相关服务
│       │   └── canvas.py         # Canvas 相关服务
│       └── providers/            # 外部 API 封装层（核心模块）
│           └── llm/              # LLM 提供商
│               ├── __init__.py   # 模块导出
│               ├── base.py       # BaseLLMProvider 抽象基类
│               └── zhipu.py      # ZhipuProvider 实现
└── tests/                        # 测试目录
    ├── conftest.py               # Pytest 配置（待实现）
    └── llm/                      # LLM 测试
        └── test_zhipu.py         # ZhipuProvider 测试
```