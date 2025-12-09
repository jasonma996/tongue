#!/bin/bash

# GitHub推送脚本 - AI舌象分析平台

echo "=================================="
echo "🚀 GitHub推送助手"
echo "=================================="
echo ""

# 检查是否已配置remote
if git remote | grep -q origin; then
    echo "✅ 远程仓库已配置"
    git remote -v
    echo ""

    read -p "是否要推送到现有仓库? (y/n): " confirm
    if [ "$confirm" != "y" ]; then
        echo "已取消推送"
        exit 0
    fi
else
    echo "⚠️  尚未配置远程仓库"
    echo ""
    echo "请先在GitHub创建仓库: https://github.com/new"
    echo ""
    echo "建议仓库名: tongue-analysis 或 ai-tongue-health"
    echo ""
    read -p "请输入你的GitHub用户名: " username
    read -p "请输入仓库名称: " reponame

    echo ""
    echo "选择推送方式:"
    echo "1) HTTPS (需要Personal Access Token)"
    echo "2) SSH (需要SSH密钥配置)"
    read -p "请选择 (1/2): " method

    if [ "$method" = "2" ]; then
        # SSH方式
        remote_url="git@github.com:$username/$reponame.git"
    else
        # HTTPS方式
        remote_url="https://github.com/$username/$reponame.git"
    fi

    echo ""
    echo "添加远程仓库: $remote_url"
    git remote add origin "$remote_url"

    if [ $? -ne 0 ]; then
        echo "❌ 添加远程仓库失败"
        exit 1
    fi
    echo "✅ 远程仓库添加成功"
fi

echo ""
echo "=================================="
echo "📤 开始推送..."
echo "=================================="
echo ""

# 获取当前分支名
current_branch=$(git branch --show-current)
echo "当前分支: $current_branch"
echo ""

# 推送
git push -u origin "$current_branch"

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "✅ 推送成功！"
    echo "=================================="
    echo ""

    # 获取remote URL
    remote_url=$(git remote get-url origin)

    # 转换为网页URL
    if [[ "$remote_url" == git@github.com:* ]]; then
        web_url="https://github.com/${remote_url#git@github.com:}"
        web_url="${web_url%.git}"
    else
        web_url="${remote_url%.git}"
    fi

    echo "🌐 访问你的仓库: $web_url"
    echo ""
    echo "🎉 恭喜！你的AI舌象分析平台已成功上传到GitHub！"
    echo ""
    echo "下一步建议:"
    echo "1. 访问仓库页面添加描述和topics"
    echo "2. 查看README确保显示正常"
    echo "3. 在Settings中配置GitHub Pages（如需）"
    echo "4. 邀请collaborators（如需）"
else
    echo ""
    echo "=================================="
    echo "❌ 推送失败"
    echo "=================================="
    echo ""
    echo "常见问题:"
    echo "1. 如果提示认证失败，请使用Personal Access Token"
    echo "   获取地址: https://github.com/settings/tokens"
    echo ""
    echo "2. 如果是SSH问题，请配置SSH密钥"
    echo "   参考: GITHUB_SETUP.md"
    echo ""
    echo "3. 如果仓库不存在，请先在GitHub创建"
    echo "   访问: https://github.com/new"
    echo ""
    echo "详细说明请查看: GITHUB_SETUP.md"
fi
