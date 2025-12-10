# DeepSeek 3.2 集成指南

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install openai opencv-python numpy
```

### 2. 设置 API Key

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，添加你的 DeepSeek API Key：

```
DEEPSEEK_API_KEY=sk-your-api-key-here
```

### 3. 运行应用

```bash
python3 app.py
```

访问: http://localhost:5001

## 💰 成本优势

| 模型 | 单次分析成本 | 说明 |
|------|------------|------|
| **OpenCV + DeepSeek 3.2** | **$0.001** | ✅ 最便宜 |
| Claude Vision | $0.02 | 20x 更贵 |
| DeepSeek VL2 (视觉模型) | $4.80 | 4800x 更贵 ⚠️ |

## 🔍 工作原理

```
用户上传舌象照片
    ↓
OpenCV 提取图像特征
 - 舌质颜色分析 (HSV色彩空间)
 - 舌苔厚薄检测 (纹理分析)
 - 舌形识别 (轮廓检测)
 - 舌面纹理 (齿痕/裂纹)
    ↓
DeepSeek 3.2 文本分析
 - 基于特征做中医体质判断
 - 生成健康评分和建议
 - 推荐饮食、穴位、中药
    ↓
返回完整健康报告
```

## 📊 特征提取示例

```python
{
  "tongue_color": {
    "type": "淡红舌",
    "description": "舌色淡红润泽，属于健康舌象"
  },
  "coating": {
    "thickness": "薄白苔",
    "color": "白苔",
    "description": "白苔，薄白苔"
  },
  "shape": {
    "type": "舌形正常",
    "description": "舌形正常"
  },
  "texture": {
    "has_teeth_marks": false,
    "features": ["表面光滑"]
  }
}
```

## ⚙️ 切换其他 AI 提供商

在 `app.py` 中修改：

```python
# 使用 DeepSeek (默认，最便宜)
analyzer = TongueAnalyzer(provider="deepseek")

# 使用 Claude Vision (贵20倍，但一站式)
analyzer = TongueAnalyzer(provider="claude")

# 使用智谱AI (中国免费API)
analyzer = TongueAnalyzer(provider="zhipu")
```

## 🐛 常见问题

### Q: ModuleNotFoundError: No module named 'cv2'
```bash
pip install opencv-python
```

### Q: DeepSeek API调用失败
- 检查 `.env` 文件中的 API Key 是否正确
- 确认 API Key 有足够余额
- 检查网络连接

### Q: 想要更精准的分析？
使用 Claude Vision API（贵20倍但质量更高）或收集更多舌象数据训练自定义模型。

## 📚 API 文档

- DeepSeek API: https://api-docs.deepseek.com/
- OpenCV 文档: https://docs.opencv.org/
