#!/bin/bash
# 修复编码问题的测试运行脚本

# 设置正确的locale环境变量
export LC_ALL=C.utf8
export LANG=C.utf8
export LANGUAGE=en_US:en

echo "已设置locale环境变量:"
echo "LC_ALL=$LC_ALL"
echo "LANG=$LANG"
echo "LANGUAGE=$LANGUAGE"

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 使用虚拟环境中的Python（如果存在）
if [ -f "$PROJECT_ROOT/.venv/bin/python" ]; then
    PYTHON_CMD="$PROJECT_ROOT/.venv/bin/python"
    echo "使用虚拟环境Python: $PYTHON_CMD"
else
    PYTHON_CMD="python3"
    echo "使用系统Python: $PYTHON_CMD"
fi

echo "项目根目录: $PROJECT_ROOT"
echo "运行测试..."

# 运行测试
cd "$PROJECT_ROOT"
"$PYTHON_CMD" test/run_tests.py "$@"