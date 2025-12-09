# 🚀 AI舌象分析Demo - 快速启动指南

## ✨ Demo已成功部署！

你的AI舌象分析网站已经完全就绪！

---

## 🌐 访问地址

```
http://localhost:5001
```

或者如果你在远程服务器上：
```
http://你的服务器IP:5001
```

---

## 📍 当前状态

✅ **后端服务：** 运行中（Flask + 规则引擎模式）
✅ **端口：** 5001
✅ **模式：** 规则引擎（无需API密钥）
✅ **存储：** uploads/tongues/

---

## 🎯 功能演示

### 1️⃣ 查看典型案例

**访问：** http://localhost:5001/demo

展示5种常见体质的舌象案例：
- 😊 健康舌（95分）
- 😮‍💨 气虚舌（72分）
- 😰 血瘀舌（65分）
- 🥵 阴虚舌（68分）
- 😓 湿热舌（60分）

**操作：** 点击任意案例 → 查看AI分析报告

### 2️⃣ 上传真实舌象

**访问：** http://localhost:5001/

**操作步骤：**
1. 点击上传区域或拖拽图片
2. 选择舌象照片（JPG/PNG）
3. 点击"开始分析"
4. 查看个性化健康报告

### 3️⃣ 查看分析报告

报告包含：
- 🎯 健康评分（0-100分）
- 👅 舌象特征分析
- 🔬 体质类型判断
- 🍎 饮食建议（推荐+避免）
- 💡 生活建议
- ✋ 穴位按摩
- 🌿 中药食疗

---

## 🎨 特色功能

### 酷炫动画效果
- ✨ Lottie扫描动画
- 📊 GSAP数字增长动画
- 🎭 平滑过渡效果
- 📱 响应式设计

### 智能分析
- 🤖 基于中医理论的规则引擎
- 📝 详细的健康建议
- 🎯 个性化推荐
- 📈 可扩展AI接口

---

## 🔧 控制命令

### 查看运行状态
```bash
ps aux | grep tongue_demo_app
```

### 查看实时日志
```bash
tail -f server.log  # 如果有日志文件
```

### 停止服务
```bash
# 找到进程ID
ps aux | grep tongue_demo_app

# 停止服务（替换PID为实际进程ID）
kill PID
```

### 重新启动
```bash
# 停止旧服务
pkill -f tongue_demo_app

# 启动新服务
python3 tongue_demo_app.py
```

---

## 🎁 升级到AI模式

当前使用规则引擎，如果想使用真实AI分析：

### 步骤1：注册智谱AI
```
访问: https://zhipuai.cn
注册账号 → 实名认证 → 获取API Key
免费额度：2000万tokens
```

### 步骤2：安装SDK
```bash
pip3 install zhipuai --break-system-packages
```

### 步骤3：设置API密钥

**方式A：环境变量**
```bash
export AI_API_KEY="your-api-key-here"
python3 tongue_demo_app.py
```

**方式B：修改代码**
编辑 `tongue_demo_app.py` 第17行：
```python
analyzer = TongueAnalyzer(api_key="your-key", provider="zhipu")
```

### 步骤4：重启服务
```bash
pkill -f tongue_demo_app
python3 tongue_demo_app.py
```

---

## 📊 项目文件说明

```
核心文件：
├── tongue_analyzer.py          # AI分析核心引擎
├── tongue_demo_app.py           # Flask Web应用
├── TONGUE_DEMO_README.md        # 详细文档
├── start_tongue_demo.sh         # 启动脚本

前端页面：
├── templates/tongue_demo/
│   ├── index.html               # 首页（上传）
│   ├── demo.html                # 案例展示
│   └── report.html              # 分析报告

配置文件：
├── requirements_tongue_demo.txt # 依赖列表
└── QUICK_START_TONGUE_DEMO.md   # 本文件
```

---

## 🐛 常见问题

### Q1: 页面打不开？
```bash
# 检查服务是否运行
ps aux | grep tongue_demo_app

# 检查端口是否被占用
netstat -tlnp | grep 5001

# 如果端口被占用，修改 tongue_demo_app.py 最后一行的port值
```

### Q2: 上传图片失败？
```bash
# 检查uploads目录权限
ls -la uploads/tongues/

# 修复权限
chmod 755 uploads/tongues
```

### Q3: API调用失败？
```bash
# 检查API密钥是否正确
echo $AI_API_KEY

# 检查网络连接
ping zhipuai.cn

# 切换回规则引擎模式
# 在 tongue_demo_app.py 中删除 API_KEY 参数
```

---

## 📱 分享Demo

### 局域网访问
```bash
# 获取本机IP
ifconfig | grep inet

# 其他设备访问（替换为你的IP）
http://192.168.1.xxx:5001
```

### 部署到公网
```bash
# 使用ngrok（简单快速）
ngrok http 5001

# 或使用云服务器（推荐）
# 部署到阿里云/腾讯云/AWS
```

---

## 🎯 下一步建议

### 功能扩展
- [ ] 添加用户登录系统
- [ ] 历史记录追踪
- [ ] 健康趋势图表
- [ ] 社区问答功能
- [ ] 专家咨询预约
- [ ] 微信小程序版本

### 技术优化
- [ ] 使用Redis缓存
- [ ] 添加数据库（PostgreSQL）
- [ ] 图片压缩和CDN
- [ ] API速率限制
- [ ] 用户数据加密

---

## 📞 技术支持

遇到问题？
1. 查看 `TONGUE_DEMO_README.md` 详细文档
2. 检查 `tongue_demo_app.py` 运行日志
3. 访问 https://zhipuai.cn/docs 查看API文档

---

## 🎉 恭喜！

你已经成功部署了一个完整的AI舌象分析网站！

**现在就去体验吧：** http://localhost:5001

---

*Made with ❤️ | Powered by 智谱AI GLM-4V*
