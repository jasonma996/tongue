# 🚀 Push to GitHub - Setup Guide

## ✅ Git已配置完成

- ✅ Git repository initialized
- ✅ User configured: maweize027@gmail.com
- ✅ Initial commit created (16 files, 4788 lines)
- ✅ Old backup files removed

---

## 📤 方法1: 使用GitHub网页（推荐）

### Step 1: 创建GitHub仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `tongue-analysis` 或 `ai-tongue-health`
   - **Description**: AI舌象分析平台 - 健康世界 (AI Tongue Analysis Platform)
   - **Visibility**: Public 或 Private（你的选择）
   - **⚠️ 不要勾选**: Initialize with README, .gitignore, license

3. 点击 "Create repository"

### Step 2: 推送代码

GitHub会显示推送命令，或者使用以下命令：

```bash
cd /home/admin123/shiptechai/Tongue

# 添加远程仓库（替换 YOUR_USERNAME 为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/tongue-analysis.git

# 推送代码
git branch -M main
git push -u origin main
```

如果你想使用 master 分支（当前分支）：
```bash
git remote add origin https://github.com/YOUR_USERNAME/tongue-analysis.git
git push -u origin master
```

### Step 3: 输入GitHub凭据

推送时会要求输入：
- **Username**: 你的GitHub用户名
- **Password**: 使用 Personal Access Token（不是密码）

**获取Personal Access Token**:
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制token
5. 在命令行中使用token作为密码

---

## 📤 方法2: 使用GitHub CLI（需要安装）

### 安装 GitHub CLI

```bash
# Ubuntu/Debian
sudo apt install gh

# 或使用官方脚本
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 使用 gh CLI 推送

```bash
cd /home/admin123/shiptechai/Tongue

# 登录GitHub
gh auth login

# 创建仓库并推送（一键完成）
gh repo create tongue-analysis --public --source=. --remote=origin --push
```

---

## 📤 方法3: 使用SSH（更安全，推荐长期使用）

### Step 1: 生成SSH密钥

```bash
# 生成SSH密钥（使用你的邮箱）
ssh-keygen -t ed25519 -C "maweize027@gmail.com"

# 启动ssh-agent
eval "$(ssh-agent -s)"

# 添加密钥
ssh-add ~/.ssh/id_ed25519

# 复制公钥
cat ~/.ssh/id_ed25519.pub
```

### Step 2: 添加SSH密钥到GitHub

1. 访问 https://github.com/settings/ssh/new
2. Title: "Tongue Project - $(hostname)"
3. 粘贴刚才复制的公钥
4. 点击 "Add SSH key"

### Step 3: 使用SSH推送

```bash
cd /home/admin123/shiptechai/Tongue

# 添加远程仓库（SSH方式）
git remote add origin git@github.com:YOUR_USERNAME/tongue-analysis.git

# 推送
git push -u origin master
```

---

## 🔧 常见问题

### Q1: 推送时提示 "remote: Support for password authentication was removed"

**解决**: 使用Personal Access Token代替密码，或使用SSH方式

### Q2: 推送失败 "failed to push some refs"

**解决**:
```bash
git pull origin master --allow-unrelated-histories
git push -u origin master
```

### Q3: 想要修改commit信息

**解决**:
```bash
git commit --amend -m "新的commit信息"
git push -f origin master  # 强制推送（仅在还未分享给他人时使用）
```

---

## 📊 仓库信息

- **Commits**: 1
- **Files**: 16
- **Lines of Code**: 4,788
- **Languages**: Python, HTML, CSS, JavaScript
- **Size**: ~200KB

---

## 🎯 推送后的下一步

1. **添加Topics**: 在GitHub仓库设置中添加标签
   - `ai`, `health`, `tongue-diagnosis`, `flask`, `chinese-medicine`

2. **设置GitHub Pages**（可选）:
   - Settings → Pages → Source: main/master branch

3. **添加shields.io徽章**到README:
   ```markdown
   ![License](https://img.shields.io/badge/license-MIT-blue.svg)
   ![Python](https://img.shields.io/badge/python-3.8+-green.svg)
   ![Flask](https://img.shields.io/badge/flask-3.1+-red.svg)
   ```

4. **启用Discussions**: 创建社区讨论区

5. **设置Issues模板**: 方便用户反馈问题

---

**准备好了吗？选择一个方法开始推送吧！** 🚀

推荐使用 **方法1**（网页方式），最简单直接！
