# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指导。

---

## 项目概览

Muse AI Studio 是一个 AI 内容生成平台，支持多厂商 LLM/图像/视频提供商，并提供无限画布前端。

**技术栈**: Python 3.12+ / FastAPI (后端) + React 18 / TypeScript / Vite / Fabric.js (前端)

---

## 核心命令

### 后端 (Python)

```bash
# 环境配置
./scripts/setup.sh                    # 创建虚拟环境并安装依赖

# 运行测试
./scripts/test.sh                     # 所有测试
./scripts/test.sh tests/llm/          # 仅 LLM 测试
./scripts/test.sh tests/image/        # 仅图像测试
./scripts/test.sh tests/video/        # 仅视频测试
./scripts/test.sh tests/llm/test_zhipu.py -v  # 单个测试文件

# 直接使用 pytest（需要 PYTHONPATH）
PYTHONPATH=/Users/saymefat/Desktop/muse_studio pytest tests/llm/test_zhipu.py -v
```

### 前端

**依赖由根目录 `package.json` 统一管理，而非 `src/frontend/package.json`。**

```bash
pnpm install                          # 安装依赖（从根目录运行）
pnpm run dev                          # 启动开发服务器 :5173
pnpm run build                        # 构建生产版本
pnpm run preview                      # 预览生产构建
```

**访问地址**: http://localhost:5173/ (首页), http://localhost:5173/canvas (画布)

---

## 架构：Provider 模式

后端使用抽象基类模式管理 AI 提供商。所有提供商都实现在 `src/backend/providers/<type>/base.py` 中定义的统一接口。

### Provider 类型

| 类型 | 基类 | 位置 |
|------|------|------|
| LLM | `BaseLLMProvider` | `src/backend/providers/llm/` |
| 图像 | `BaseImageProvider` | `src/backend/providers/image/` |
| 视频 | `BaseVideoProvider` | `src/backend/providers/video/` |

### 添加新 Provider

按照 `docs/AI_PRD/provider_sop.md` 执行：

1. 创建 `src/backend/providers/<type>/<vendor>.py` 继承基类
2. 更新该目录下的 `__init__.py`
3. 添加配置到 `config.py` 和 `.env.example`
4. 添加包到 `requirements.txt`
5. 创建测试 `tests/<type>/test_<vendor>.py`
6. 运行 `./scripts/test.sh` 验证

### Provider 接口示例

```python
class BaseLLMProvider(ABC):
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.client = None

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass

    def is_available(self) -> bool:
        return self.client is not None
```

---

## 前端架构

### 核心设计原则

1. **扁平化结构**: types 和 store 直接放在 `src/` 下，不单独建目录
2. **相对导入**: 使用 `import './InfiniteCanvas.css'` 而非 `@/` 别名
3. **无占位文件**: 需要时再创建文件
4. **Hook 模式**: Fabric.js 封装在 `useFabricCanvas.ts` 中，兼容 React

### 画布坐标系统

```
屏幕 → 画布:  canvasX = (screenX + viewport.x) / viewport.zoom
画布 → 屏幕:  screenX = canvasX * viewport.zoom - viewport.x
```

viewport 存储 `x = -vpt[4]`（Fabric 变换的负值），数值更直观。

### 文件结构

```
src/frontend/src/
├── types.ts          # 类型 + 常量合并（单文件）
├── store.ts          # Zustand 状态（单文件）
├── pages/            # 路由组件
├── components/       # 按功能分组（如 canvas/）
└── hooks/            # 自定义 React Hooks
```

---

## 配置

- 后端配置: `src/backend/config.py` 从 `.env` 读取
- 前端配置: `vite.config.ts` 构建配置, `tsconfig.json` TypeScript 配置
- 根目录 `package.json` 管理所有前端依赖

---

## 日志

日志配置位于 `src/backend/logger.py`。输出位置：
- 控制台（彩色，生产环境 INFO 级别）
- `logs/app_YYYYMMDD.log`（结构化，DEBUG 级别）

---

## Git 约定

提交格式: `<type>: <description>`

类型: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`

# 重要注意事项
1. python环境在/muse_studio/.venv
2. 前端环境在/muse_studio/node_modules
3. 涉及环境改动要同步至package.json和requirements.txt，并检查scripts/setup.sh
4. 后端新增或修改码，要通过/muse_studio/scripts/restart.sh重启服务，需要在/muse_studio/tests保持相同目录结构、test_源文件名 进行测试，只做最简单最上层的测试，完成后要同步至scripts/test.sh
5. 所有内容完成后要同步至README.md和/muse_studio/docs/AI_PRD/architecture.md，README.md要包含简单的入门环境配置，以及提供什么模型供应商、什么功能，界面展示示例；/muse_studio/docs/AI_PRD/architecture.md要包含项目概览、核心命令、架构、配置、日志、Git 约定、重要注意事项等内容
6. 定期整理文档至/muse_studio/docs/AI_PRD
7. commit提交和push代码前要询问一下，允许后才进行操作