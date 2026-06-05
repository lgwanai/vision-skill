#!/bin/bash
# ============================================================
# vision-skill macOS 离线依赖一键安装脚本
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMMON_DIR="$SCRIPT_DIR/common"
MACOS_DIR="$SCRIPT_DIR/macos"
REQUIREMENTS="$SCRIPT_DIR/../requirements.txt"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()  { echo -e "${CYAN}[INFO]${NC}  $1"; }
log_ok()   { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_err()  { echo -e "${RED}[ERROR]${NC} $1"; }

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  vision-skill macOS 离线依赖安装${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""

# 检查 Python
PYTHON=""
for cmd in python3 python; do
    if command -v $cmd &>/dev/null; then
        version=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        major=$(echo "$version" | cut -d. -f1)
        minor=$(echo "$version" | cut -d. -f2)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
            PYTHON=$cmd
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    log_err "未找到 Python 3.10+，请先安装 Python"
    echo "    推荐: brew install python@3.12"
    exit 1
fi
log_info "使用 Python: $($PYTHON --version)"

# 检查离线包目录
if [ ! -d "$COMMON_DIR" ]; then
    log_err "离线包目录不存在: $COMMON_DIR"
    exit 1
fi
if [ ! -d "$MACOS_DIR" ]; then
    log_err "离线包目录不存在: $MACOS_DIR"
    exit 1
fi

# 检查 requirements.txt
if [ ! -f "$REQUIREMENTS" ]; then
    log_err "requirements.txt 不存在: $REQUIREMENTS"
    exit 1
fi

# 统计离线包
common_count=$(find "$COMMON_DIR" -name "*.whl" -o -name "*.tar.gz" | wc -l | tr -d ' ')
macos_count=$(find "$MACOS_DIR" -name "*.whl" -o -name "*.tar.gz" | wc -l | tr -d ' ')
log_info "离线包: common $common_count 个 + macos $macos_count 个"

# 安装
echo ""
log_info "开始离线安装..."
echo ""

$PYTHON -m pip install --no-index \
    --find-links "$COMMON_DIR" \
    --find-links "$MACOS_DIR" \
    -r "$REQUIREMENTS"

echo ""
log_ok "安装完成!"

# 验证
echo ""
log_info "验证已安装的包:"
$PYTHON -c "
import importlib.metadata, sys
pkgs = {
    'requests': 'requests',
    'python-dotenv': 'dotenv',
    'cos-python-sdk-v5': 'qcloud_cos',
    'charset-normalizer': 'charset_normalizer',
    'urllib3': 'urllib3',
    'certifi': 'certifi',
    'idna': 'idna',
    'xmltodict': 'xmltodict',
    'pycryptodome': 'Crypto',
    'six': 'six',
    'crcmod': 'crcmod',
}
all_ok = True
for name, mod in pkgs.items():
    try:
        ver = importlib.metadata.version(name)
        __import__(mod)
        print(f'  \033[32m✓\033[0m {name:25s} {ver}')
    except Exception as e:
        print(f'  \033[31m✗\033[0m {name:25s} 未安装')
        all_ok = False
if all_ok:
    print()
    print('  \033[32m所有依赖验证通过!\033[0m')
else:
    print()
    print('  \033[31m部分依赖缺失，请检查\033[0m')
    sys.exit(1)
"

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  所有依赖已就绪!${NC}"
echo -e "${GREEN}============================================${NC}"
