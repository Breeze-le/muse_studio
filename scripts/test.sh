#!/bin/bash
# muse_studio 测试运行脚本
# 用法: ./scripts/test.sh [测试文件模式] [选项]

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # 无颜色

# 项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# 日志目录
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/test_$TIMESTAMP.log"

# 默认测试模式 (使用新的 llm 测试结构)
TEST_PATTERN="${1:-tests/}"
PYTEST_OPTIONS="${2:--v}"

echo -e "${GREEN}========== muse_studio 测试运行 ==========${NC}"
echo -e "${YELLOW}测试模式: ${TEST_PATTERN}${NC}"
echo -e "${YELLOW}测试选项: ${PYTEST_OPTIONS}${NC}"
echo -e "${YELLOW}日志文件: ${LOG_FILE}${NC}"
echo ""

# 检查 pytest 是否已安装
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}pytest 未安装，正在安装...${NC}"
    pip install pytest pytest-cov -q
fi

# 运行测试，启用日志输出和文件记录
python -m pytest "${TEST_PATTERN}" ${PYTEST_OPTIONS} \
    --log-cli-level=INFO \
    --log-cli-format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' \
    --log-file="$LOG_FILE" \
    --log-file-level=INFO \
    --log-file-format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' \
    --cov=src \
    --cov-report=term-missing \
    --cov-report=html

echo ""
echo -e "${GREEN}========== 测试完成 ==========${NC}"
echo -e "${BLUE}覆盖率报告: htmlcov/index.html${NC}"
echo -e "${BLUE}测试日志: ${LOG_FILE}${NC}"
echo ""
echo -e "${YELLOW}快捷命令:${NC}"
echo -e "  ${BLUE}./scripts/test.sh tests/llm/${NC}         # 仅运行 llm 测试"
echo -e "  ${BLUE}./scripts/test.sh tests/image/${NC}       # 仅运行 image 测试"
echo -e "  ${BLUE}./scripts/test.sh tests/llm/test_*.py${NC}  # 运行指定测试文件"
echo -e "  ${BLUE}tail -f logs/test_*.log${NC}              # 查看实时日志"
