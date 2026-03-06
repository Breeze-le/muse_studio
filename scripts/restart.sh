#!/bin/bash
# Muse Studio 服务重启脚本
# 用法: bash scripts/restart.sh [backend|frontend]

set -e

# 项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$(dirname "$SCRIPT_DIR")"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 解析参数
SERVICE="${1:-all}"

case $SERVICE in
    backend)
        START_BACKEND=true
        START_FRONTEND=false
        ;;
    frontend)
        START_BACKEND=false
        START_FRONTEND=true
        ;;
    all)
        START_BACKEND=true
        START_FRONTEND=true
        ;;
    *)
        echo "用法: bash scripts/restart.sh [backend|frontend|all]"
        exit 1
        ;;
esac

# 创建日志目录
mkdir -p logs

# ========== 停止服务 ==========
echo "🛑 停止服务..."

if [ "$START_BACKEND" = true ]; then
    PID=$(lsof -ti:8000 2>/dev/null || true)
    [ -n "$PID" ] && kill -9 $PID 2>/dev/null || true
    echo -e "${GREEN}  ✓ 后端端口 8000 已释放${NC}"
fi

if [ "$START_FRONTEND" = true ]; then
    PID=$(lsof -ti:5173 2>/dev/null || true)
    [ -n "$PID" ] && kill -9 $PID 2>/dev/null || true
    echo -e "${GREEN}  ✓ 前端端口 5173 已释放${NC}"
fi

echo ""

# ========== 启动服务 ==========
if [ "$START_BACKEND" = true ]; then
    echo "🚀 启动后端服务..."
    source .venv/bin/activate
    nohup python -m uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --reload > logs/backend.log 2>&1 &
    sleep 2
    echo -e "${GREEN}  ✓ 后端: http://localhost:8000/docs${NC}"
    echo ""
fi

if [ "$START_FRONTEND" = true ]; then
    echo "🚀 启动前端服务..."
    PKG_MANAGER=$(command -v pnpm &> /dev/null && echo "pnpm" || echo "npm")
    nohup $PKG_MANAGER run dev > logs/frontend.log 2>&1 &
    sleep 2
    echo -e "${GREEN}  ✓ 前端: http://localhost:5173${NC}"
    echo ""
fi

echo "✅ 完成"
echo "   日志: tail -f logs/backend.log 或 logs/frontend.log"
