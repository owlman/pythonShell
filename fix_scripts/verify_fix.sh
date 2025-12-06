#!/bin/bash
# 简单的测试验证脚本

# 设置正确的locale环境变量
export LC_ALL=C.utf8
export LANG=C.utf8
export LANGUAGE=en_US:en

echo "验证编码修复效果..."
echo "Python版本:"
python3 --version

echo -e "\n运行单个测试验证:"
cd "$(dirname "$0")"
python3 -m pytest test/test_common.py::TestPrintBanner::test_print_banner_default_width -v

echo -e "\n检查项目构建:"
python3 -c "import sys; sys.path.insert(0, 'src'); import common; common.print_banner('编码修复验证成功！')"