#!/bin/bash

# AI舌象分析Demo启动脚本

echo "=================================="
echo "🔬 AI舌象分析Demo启动工具"
echo "=================================="
echo ""

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if (( $(echo "$python_version < 3.8" | bc -l) )); then
    echo "❌ Python版本过低，需要3.8+，当前版本：$python_version"
    exit 1
fi
echo "✅ Python版本检查通过：$python_version"

# 检查依赖
echo ""
echo "📦 检查依赖..."

if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask未安装，正在安装..."
    pip3 install flask
fi
echo "✅ Flask已安装"

# 询问是否使用AI模式
echo ""
echo "请选择运行模式："
echo "1) 规则引擎模式（无需API，立即使用）"
echo "2) AI模式（需要智谱AI API Key）"
echo ""
read -p "请输入选择 (1/2): " mode_choice

if [ "$mode_choice" = "2" ]; then
    # AI模式
    if ! python3 -c "import zhipuai" 2>/dev/null; then
        echo "⚠️  zhipuai SDK未安装，正在安装..."
        pip3 install zhipuai
    fi
    echo "✅ zhipuai已安装"

    if [ -z "$AI_API_KEY" ]; then
        echo ""
        echo "请输入智谱AI API Key："
        echo "（如果还没有，请访问 https://zhipuai.cn 注册获取）"
        read -p "API Key: " api_key
        export AI_API_KEY="$api_key"
    fi

    if [ -z "$AI_API_KEY" ]; then
        echo "❌ 未设置API Key，退出..."
        exit 1
    fi
    echo "✅ API Key已设置"
fi

# 创建上传目录
echo ""
echo "📁 创建上传目录..."
mkdir -p uploads/tongues
echo "✅ 目录创建完成"

# 启动应用
echo ""
echo "=================================="
echo "🚀 启动服务..."
echo "=================================="
echo ""
echo "访问地址: http://localhost:5001"
echo "按 Ctrl+C 停止服务"
echo ""

python3 app.py
