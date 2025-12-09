# 🌍 AI舌象分析 - 健康世界

> **"舌观世界，洞见自己"**
> 每一个舌象都值得被认真对待，当十亿个舌象汇聚在一起，它们组成了人类健康的完整地图。

---

## 📖 项目简介

这是一个创新的AI健康分析平台，通过舌象分析作为流量入口，引导用户进入丰富的健康内容社区。

### 核心特点

- 🔬 **AI舌象分析** - 30秒快速生成个性化健康报告
- 🗺️ **健康地图** - 可视化你的健康状态（压力火山区、疲劳高原区、湿气沼泽区）
- 🌟 **健康星球** - 加入你的星球社区，与相似体质的人交流
- 📚 **内容推荐** - 基于体质的个性化健康内容
- 💫 **改善追踪** - 记录健康改善旅程

---

## 🚀 快速开始

### 方法1：使用启动脚本（推荐）

```bash
cd Tongue
./start.sh
```

脚本会自动：
- 检查Python版本
- 安装必要依赖
- 选择运行模式（规则引擎/AI模式）
- 启动服务器

### 方法2：手动启动

```bash
cd Tongue

# 安装依赖
pip3 install -r requirements.txt

# 启动应用
python3 app.py
```

### 访问应用

```
🌐 主页: http://localhost:5001
🌟 星球探索: http://localhost:5001/demo
📊 报告示例: http://localhost:5001/report
```

---

## 📁 项目结构

```
Tongue/
├── app.py                  # Flask主应用
├── analyzer.py             # AI分析引擎
├── requirements.txt        # Python依赖
├── start.sh               # 快速启动脚本
├── .env.example           # 环境变量示例
│
├── templates/             # HTML模板
│   └── tongue_demo/
│       ├── index.html     # 首页（上传界面）
│       ├── demo.html      # 星球探索页
│       ├── report.html    # 分析报告页
│       └── about.html     # 关于页面
│
├── uploads/               # 上传文件存储
│   └── tongues/           # 舌象图片
│
├── static/                # 静态资源
│   ├── css/
│   ├── js/
│   └── images/
│
└── docs/                  # 文档
    ├── README.md          # 技术文档
    ├── QUICK_START.md     # 快速入门
    ├── HEALTH_WORLD_CONCEPT.md      # 健康世界设计理念
    ├── TRAFFIC_TO_CONTENT_STRATEGY.md  # 流量转化策略
    └── UPDATE_SUMMARY.md  # 更新日志
```

---

## 🎯 三层架构

### 1️⃣ 个体层：健康地图

每个人的舌象转化为独特的健康地形图：

```
你的健康地图
├─ 🌋 压力火山区（舌尖红）
├─ 🏔️ 疲劳高原区（舌体胖大）
└─ 🌊 湿气沼泽区（舌苔厚腻）
```

### 2️⃣ 社群层：健康星球

相似体质的人组成星球社区：

```
🌕 健康星球（95-100分）- 2.3万居民
🪐 气虚星球（70-79分）- 15.7万居民
🔴 血瘀星球（60-69分）- 8.9万居民
🌙 阴虚星球（65-75分）- 11.2万居民
🌑 湿热星球（55-65分）- 12.1万居民
```

### 3️⃣ 宏观层：世界健康地图

聚合数据展示群体健康趋势（未来功能）

---

## ⚙️ 配置说明

### AI模式配置

创建 `.env` 文件（参考 `.env.example`）：

```bash
# 智谱AI API Key（可选）
AI_API_KEY=your_api_key_here

# 支持的AI提供商: zhipu, qwen
AI_PROVIDER=zhipu
```

**获取免费API Key**:
- 智谱AI: https://zhipuai.cn （新用户2000万免费tokens）
- 通义千问: https://dashscope.aliyun.com

### 规则引擎模式

无需API Key，使用内置规则引擎，立即可用！

---

## 🛠️ 技术栈

### 后端
- **Flask** - Python Web框架
- **智谱AI GLM-4V-Flash** - 免费视觉AI模型
- **规则引擎** - Fallback分析系统

### 前端
- **HTML5/CSS3/JavaScript** - 原生Web技术
- **Inter字体** - 现代排版
- **Glassmorphism** - 玻璃态设计
- **Lottie** - JSON动画
- **GSAP** - 高性能动画库

---

## 📊 用户旅程

```
1. 上传舌象照片
   ↓
2. AI智能分析（30秒）
   ↓
3. 查看个人健康地图
   ↓
4. 自动分配到对应星球
   ↓
5. 浏览个性化内容推荐
   ↓
6. 加入社区（未来）
```

---

## 📚 文档索引

- [技术文档](docs/README.md) - 详细技术说明
- [快速入门](docs/QUICK_START.md) - 5分钟上手指南
- [健康世界概念](docs/HEALTH_WORLD_CONCEPT.md) - 产品设计哲学
- [流量转化策略](docs/TRAFFIC_TO_CONTENT_STRATEGY.md) - 商业模式
- [更新日志](docs/UPDATE_SUMMARY.md) - 最新更新

---

## 🔜 路线图

### Phase 1: 核心功能 ✅
- [x] AI舌象分析
- [x] 健康地图可视化
- [x] 健康星球系统
- [x] 内容推荐引擎

### Phase 2: 内容系统 🚧
- [ ] 博客文章系统
- [ ] 文章分类筛选
- [ ] 搜索功能
- [ ] SEO优化

### Phase 3: 社区功能 📅
- [ ] 用户注册/登录
- [ ] 故事发布
- [ ] 点赞/评论
- [ ] 星球广场

### Phase 4: 数据可视化 📅
- [ ] 世界健康地图
- [ ] 城市健康排行
- [ ] 实时数据大屏
- [ ] 趋势分析

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)（待创建）

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 💡 愿景

> **"我们相信，每一个舌象都值得被认真对待。**
>
> **当十亿个舌象汇聚在一起，**
> **它们组成了人类健康的完整地图。**
>
> **通过这张地图，**
> **我们不仅能看见自己的健康状态，**
> **更能看见整个人类的健康脉搏。**
>
> **这就是我们正在创造的——**
> **一个由舌头组成的健康世界。"**

---

**由 ❤️ 和 AI 共同创造**
