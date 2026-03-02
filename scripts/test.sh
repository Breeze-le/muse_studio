#!/bin/bash
# muse_studio 测试运行脚本
# 用法: bash scripts/test.sh [测试路径] [pytest选项]

set -e

# 项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$(dirname "$SCRIPT_DIR")"

# 激活虚拟环境
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# 日志目录
mkdir -p logs
LOG_FILE="logs/test_$(date +"%Y%m%d_%H%M%S").log"

# 默认参数
TEST_PATTERN="${1:-tests/}"
PYTEST_OPTIONS="${2:--v}"

echo "测试模式: ${TEST_PATTERN}"
echo "日志文件: ${LOG_FILE}"
echo ""

# 运行测试
python -m pytest "${TEST_PATTERN}" ${PYTEST_OPTIONS} \
    --log-cli-level=INFO \
    --log-file="$LOG_FILE" \
    --log-file-level=INFO

echo ""
echo "测试完成。日志: ${LOG_FILE}"
echo ""
echo "使用示例:"
echo "  bash scripts/test.sh                          # 运行所有测试"
echo "  bash scripts/test.sh tests/llm/               # 仅运行 llm 测试"
echo "  bash scripts/test.sh tests/image/             # 仅运行 image 测试"
echo "  bash scripts/test.sh tests/video/             # 仅运行 video 测试"
echo "  bash scripts/test.sh tests/image/test_*.py -v # 运行指定测试"
