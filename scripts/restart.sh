#!/bin/bash
# Muse Studio 前端重启脚本
# 用途: 停止当前运行的前端服务并重新启动

set -e

# 获取脚本所在目录和项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "🔄 Muse Studio 前端重启脚本"
echo "项目根目录: $PROJECT_ROOT"
echo ""

# 前端默认端口
VITE_PORT=5173

# 解析参数
PORT=$VITE_PORT
while [[ $# -gt 0 ]]; do
    case $1 in
        --port|-p)
            PORT="$2"
            shift 2
            ;;
        *)
            echo "用法: bash scripts/restart.sh [--port|-p <port>]"
            exit 1
            ;;
    esac
done

# ========== 停止服务 ==========
echo "🛑 停止现有前端服务..."

# 查找占用端口的进程
PID=$(lsof -ti:$PORT 2>/dev/null || true)

if [ -n "$PID" ]; then
    echo -e "${YELLOW}停止端口 $PORT 上的服务 (PID $pid)...${NC}"
    kill -9 $PID 2>/dev/null || true
    sleep 1
    echo -e "${GREEN}✓ 服务已停止${NC}"
else
    echo -e "${GREEN}✓ 端口 $PORT 未被占用${NC}"
fi

echo ""

# ========== 启动服务 ==========
echo "🚀 启动前端开发服务器..."

# 检查包管理器
cd "$PROJECT_ROOT"

if command -v pnpm &> /dev/null; then
    PKG_MANAGER="pnpm"
elif command -v npm &> /dev/null; then
    PKG_MANAGER="npm"
else
    echo -e "${RED}✗ 错误: 未安装 pnpm 或 npm${NC}"
    exit 1
fi

echo -e "${GREEN}使用 $PKG_MANAGER 启动服务...${NC}"

# 创建日志目录
mkdir -p logs

# 后台启动前端服务器
LOG_FILE="logs/frontend_$(date +"%Y%m%d_%H%M%S").log"
nohup $PKG_MANAGER run dev > "$LOG_FILE" 2>&1 &
NEW_PID=$!

sleep 2

echo ""
echo "✅ 前端服务已启动"
echo ""
echo "   访问: http://localhost:5173"
echo "   日志: ls -lt logs/"
echo ""
echo "   停止: lsof -ti:5173 | xargs kill -9"
