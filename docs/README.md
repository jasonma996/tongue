# 🔬 AI舌象分析 Demo Web

一个酷炫的AI驱动的舌象健康分析演示网站

![Status](https://img.shields.io/badge/Status-Ready-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ 功能特点

- 🤖 **AI智能分析** - 支持智谱AI GLM-4V（免费）和规则引擎双模式
- 📸 **拖拽上传** - 支持拖拽或点击上传舌象照片
- 🎨 **酷炫动画** - Lottie动画 + GSAP，流畅的用户体验
- 📊 **可视化报告** - 动态展示健康评分和详细建议
- 🌿 **中医调理** - 提供饮食、穴位、中药等全方位建议
- 📱 **响应式设计** - 支持PC和移动设备
- 🎯 **典型案例库** - 5种常见体质的舌象案例演示

## 🚀 快速开始

### 方式1：规则引擎模式（无需API）

```bash
# 1. 安装依赖
pip install flask

# 2. 启动服务
python tongue_demo_app.py

# 3. 访问网站
打开浏览器访问: http://localhost:5001
```

**注意：** 规则引擎模式使用预设规则分析，用于演示和测试。

### 方式2：AI模式（推荐）

```bash
# 1. 注册智谱AI账号
访问 https://zhipuai.cn
注册并获取API Key（新用户送2000万tokens）

# 2. 安装依赖
pip install flask zhipuai

# 3. 设置API密钥
export AI_API_KEY="your-zhipu-api-key"

# 或者在代码中设置
# 编辑 tongue_demo_app.py, 修改:
# analyzer = TongueAnalyzer(api_key="your-key", provider="zhipu")

# 4. 启动服务
python tongue_demo_app.py

# 5. 访问网站
打开浏览器访问: http://localhost:5001
```

## 📁 项目结构

```
shiptechai/
├── tongue_analyzer.py          # AI舌象分析器核心代码
├── tongue_demo_app.py           # Flask Web应用
├── templates/
│   └── tongue_demo/
│       ├── index.html           # 首页（上传页面）
│       ├── demo.html            # 典型案例展示
│       └── report.html          # 分析报告页面
├── static/
│   ├── css/                     # 样式文件
│   ├── js/                      # JavaScript文件
│   └── animations/              # 动画资源
└── uploads/tongues/             # 上传的图片存储目录
```

## 🎯 使用方式

### 1. 上传分析

1. 访问首页 http://localhost:5001
2. 点击或拖拽上传舌象照片
3. 点击"开始分析"
4. 查看AI生成的健康报告

### 2. 查看案例

1. 点击首页的"查看典型舌象案例演示"
2. 选择任意案例（健康舌、气虚舌、血瘀舌等）
3. 查看AI分析报告

## 🔧 配置选项

### 支持的AI提供商

在 `tongue_analyzer.py` 中：

```python
# 智谱AI（推荐，免费）
analyzer = TongueAnalyzer(api_key="your-key", provider="zhipu")

# 通义千问
analyzer = TongueAnalyzer(api_key="your-key", provider="qwen")

# 规则引擎（无需API）
analyzer = TongueAnalyzer()  # 自动使用规则引擎
```

### 修改端口

在 `tongue_demo_app.py` 中：

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # 修改port值
```

## 📊 典型案例说明

| 案例类型 | 舌象特征 | 健康评分 | 主要建议 |
|---------|---------|---------|---------|
| 健康舌 | 淡红舌质，薄白苔 | 95 | 保持良好习惯 |
| 气虚舌 | 舌体胖大，舌边齿痕 | 72 | 补气健脾，避免过劳 |
| 血瘀舌 | 舌质暗紫，有瘀点 | 65 | 活血化瘀，增加运动 |
| 阴虚舌 | 舌红少苔，有裂纹 | 68 | 滋阴润燥，避免熬夜 |
| 湿热舌 | 舌苔黄腻，舌质红 | 60 | 清热祛湿，饮食清淡 |

## 🎨 技术栈

### 后端
- **Flask** - Web框架
- **智谱AI GLM-4V** - 图像识别和分析
- **Python 3.8+**

### 前端
- **原生HTML/CSS/JavaScript** - 无框架依赖
- **Lottie-web** - 动画效果
- **GSAP** - 数字动画
- **Chart.js** - 数据可视化（未来功能）

## 💰 成本分析

### 规则引擎模式
- **成本：** 完全免费
- **限制：** 使用预设规则，无真实AI分析

### 智谱AI模式
- **免费额度：** 新用户2000万tokens（约1-2万次分析）
- **付费价格：** 超出后也是免费（GLM-4V-Flash长期免费）
- **成本估算：** **$0/月**

### 通义千问模式
- **价格：** ¥0.003/1K tokens
- **成本估算：** 每次分析约¥0.006（1000用户/月 = ¥18）

## 🔒 隐私和安全

- ✅ 上传的图片仅用于分析
- ✅ 图片存储在本地服务器
- ✅ 可以定期清理上传目录
- ✅ 不会存储用户个人信息

## 📝 待办功能

- [ ] 用户账号系统
- [ ] 历史记录追踪
- [ ] 健康趋势对比
- [ ] 微信/支付宝登��
- [ ] 专家咨询预约
- [ ] 社区问答功能
- [ ] 移动端APP

## 🐛 故障排除

### 问题1：启动失败

```bash
# 检查Python版本
python --version  # 需要3.8+

# 重新安装依赖
pip install --upgrade flask zhipuai
```

### 问题2：API调用失败

```bash
# 检查API密钥是否正确
echo $AI_API_KEY

# 检查网络连接
ping zhipuai.cn
```

### 问题3：上传文件失败

```bash
# 确保uploads目录存在且有写权限
mkdir -p uploads/tongues
chmod 755 uploads/tongues
```

## 📞 联系方式

- **问题反馈：** 在GitHub提Issue
- **功能建议：** 欢迎提Pull Request

## 📄 许可证

MIT License - 可自由使用和修改

## 🙏 致谢

- 智谱AI提供免费的Vision API
- Lottie动画库
- GSAP动画引擎
- 所有开源贡献者

---

**Made with ❤️ for better health**

🚀 **立即开始使用：** `python tongue_demo_app.py`
