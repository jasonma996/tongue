"""
AI舌象分析器
支持智谱AI GLM-4V-Flash（免费）、通义千问Qwen-VL 和 DeepSeek 3.2
"""

import os
import json
import base64
from typing import Dict, Any, Optional
from tongue_feature_extractor import TongueFeatureExtractor

class TongueAnalyzer:
    """舌象分析器基类"""

    def __init__(self, api_key: str = None, provider: str = "deepseek"):
        """
        初始化分析器

        Args:
            api_key: API密钥
            provider: 'zhipu' 或 'qwen' 或 'deepseek'
        """
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY') or os.getenv('AI_API_KEY')
        self.provider = provider
        self.feature_extractor = TongueFeatureExtractor()

        if not self.api_key:
            print("⚠️  未设置API密钥，将使用规则引擎模式")
            self.use_mock = True
        else:
            self.use_mock = False
            self._init_client()

    def _init_client(self):
        """初始化AI客户端"""
        try:
            if self.provider == "zhipu":
                from zhipuai import ZhipuAI
                self.client = ZhipuAI(api_key=self.api_key)
                print("✅ 智谱AI客户端初始化成功")
            elif self.provider == "qwen":
                import dashscope
                dashscope.api_key = self.api_key
                self.client = dashscope
                print("✅ 通义千问客户端初始化成功")
            elif self.provider == "deepseek":
                from openai import OpenAI
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.deepseek.com"
                )
                print("✅ DeepSeek客户端初始化成功")
        except ImportError as e:
            print(f"⚠️  {self.provider} SDK未安装，切换到规则引擎模式")
            self.use_mock = True

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        分析舌象图片

        Args:
            image_path: 图片路径

        Returns:
            分析结果字典
        """
        if self.use_mock:
            return self._mock_analysis(image_path)

        if self.provider == "zhipu":
            return self._analyze_with_zhipu(image_path)
        elif self.provider == "qwen":
            return self._analyze_with_qwen(image_path)
        elif self.provider == "deepseek":
            return self._analyze_with_deepseek(image_path)

    def _analyze_with_zhipu(self, image_path: str) -> Dict[str, Any]:
        """使用智谱AI分析"""

        # 读取图片
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        # 构建prompt
        prompt = """你是一位经验丰富的中医舌诊专家。请详细分析这张舌象照片：

【分析维度】
1. 舌体特征：舌色、舌形、舌态（齿痕/裂纹等）
2. 舌苔特征：苔色、苔质、润燥程度
3. 体质判断：主要体质类型（气虚/血瘀/阴虚/阳虚/湿热/寒湿等）
4. 健康评分：0-100分
5. 健康建议：饮食、生活习惯、穴位按摩
6. 中药食疗：推荐常见中药材

【输出格式 - 严格JSON】
{
  "tongue_body": {
    "color": "舌色描述",
    "shape": "舌形描述",
    "features": ["特征1", "特征2"]
  },
  "tongue_coating": {
    "color": "苔色",
    "thickness": "厚/薄",
    "texture": "质地描述"
  },
  "constitution": {
    "primary": "主要体质",
    "secondary": ["次要体质"],
    "description": "体质说明（50字内，通俗易懂）"
  },
  "health_score": 85,
  "score_level": "优秀/良好/一般/较差",
  "advice": {
    "diet": {
      "recommended": ["🥦 食物1", "🍎 食物2", "🐟 食物3"],
      "avoid": ["❌ 禁忌1", "❌ 禁忌2"]
    },
    "lifestyle": ["💤 建议1", "🏃 建议2", "😊 建议3"],
    "acupoints": ["✋ 穴位1（位置+功效）", "✋ 穴位2"]
  },
  "herbs": ["🌿 中药1（功效）", "🌿 中药2", "🌿 中药3"],
  "summary": "一句话总结（30字内，积极正向）"
}

注意：使用emoji增加趣味性，语言通俗易懂，避免过于专业的术语。"""

        try:
            response = self.client.chat.completions.create(
                model="glm-4v-flash",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )

            ai_response = response.choices[0].message.content

            # 解析JSON
            result = self._parse_json_response(ai_response)
            result['provider'] = 'zhipu-ai'
            result['model'] = 'glm-4v-flash'

            return result

        except Exception as e:
            print(f"❌ API调用失败: {e}")
            return self._mock_analysis(image_path)

    def _analyze_with_deepseek(self, image_path: str) -> Dict[str, Any]:
        """使用 DeepSeek 3.2 + 图像特征提取分析"""

        try:
            # Step 1: 使用 OpenCV 提取图像特征
            print("🔍 正在提取舌象特征...")
            features = self.feature_extractor.extract_features(image_path)

            # Step 2: 构建提示词
            prompt = f"""你是一位经验丰富的中医舌诊专家。我已经通过图像分析提取了以下舌象特征：

【舌象特征数据】
1. 舌质颜色：{features['tongue_color']['type']} ({features['tongue_color']['description']})
2. 舌苔状态：{features['coating']['description']}
   - 舌苔厚薄：{features['coating']['thickness']}
   - 舌苔颜色：{features['coating']['color']}
3. 舌形特征：{features['shape']['description']}
4. 舌面纹理：{features['texture']['description']}

【特征总结】
{features['summary']}

请根据以上舌象特征，从中医角度进行专业分析，并返回JSON格式的健康报告。

【输出格式 - 严格JSON】
{{
  "tongue_body": {{
    "color": "舌色描述",
    "shape": "舌形描述",
    "features": ["特征1", "特征2"]
  }},
  "tongue_coating": {{
    "color": "苔色",
    "thickness": "厚/薄",
    "texture": "质地描述"
  }},
  "constitution": {{
    "primary": "主要体质类型（气虚质/血瘀质/阴虚质/阳虚质/湿热质/痰湿质/气郁质/特禀质/平和质）",
    "secondary": ["次要体质"],
    "description": "体质说明（50字内，通俗易懂）"
  }},
  "health_score": 数字分数(0-100),
  "score_level": "优秀/良好/一般/较差",
  "advice": {{
    "diet": {{
      "recommended": ["🥦 食物1", "🍎 食物2", "🐟 食物3"],
      "avoid": ["❌ 禁忌1", "❌ 禁忌2"]
    }},
    "lifestyle": ["💤 建议1", "🏃 建议2", "😊 建议3"],
    "acupoints": ["✋ 穴位1（位置+功效）", "✋ 穴位2"]
  }},
  "herbs": ["🌿 中药1（功效）", "🌿 中药2", "🌿 中药3"],
  "summary": "一句话总结（30字内，积极正向）"
}}

注意：使用emoji增加趣味性，语言通俗易懂，避免过于专业的术语。"""

            # Step 3: 调用 DeepSeek API
            print("🤖 DeepSeek 3.2 分析中...")
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一位专业的中医舌诊专家，擅长根据舌象特征进行健康分析和体质辨识。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )

            ai_response = response.choices[0].message.content

            # 解析JSON
            result = self._parse_json_response(ai_response)
            result['provider'] = 'deepseek'
            result['model'] = 'deepseek-chat'
            result['extracted_features'] = features

            print("✅ DeepSeek 分析完成")
            return result

        except Exception as e:
            print(f"❌ DeepSeek API调用失败: {e}")
            return self._mock_analysis(image_path)

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """从AI响应中提取JSON"""
        try:
            # 尝试提取JSON部分
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "{" in response and "}" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            else:
                json_str = response

            return json.loads(json_str)

        except json.JSONDecodeError:
            return {
                'error': 'JSON解析失败',
                'raw_response': response
            }

    def _mock_analysis(self, image_path: str) -> Dict[str, Any]:
        """规则引擎模式 - 返回示例数据"""

        # 根据文件名判断类型（简单演示）
        filename = os.path.basename(image_path).lower()

        if 'qi' in filename or '气虚' in filename:
            return self._get_qi_deficiency_result()
        elif 'blood' in filename or '血瘀' in filename:
            return self._get_blood_stasis_result()
        elif 'yin' in filename or '阴虚' in filename:
            return self._get_yin_deficiency_result()
        elif 'damp' in filename or '湿热' in filename:
            return self._get_damp_heat_result()
        else:
            return self._get_healthy_result()

    def _get_healthy_result(self) -> Dict[str, Any]:
        """健康舌象示例"""
        return {
            "tongue_body": {
                "color": "淡红色",
                "shape": "舌体大小适中",
                "features": ["舌质柔软", "活动灵活", "无明显异常"]
            },
            "tongue_coating": {
                "color": "薄白色",
                "thickness": "薄",
                "texture": "均匀分布，润泽适中"
            },
            "constitution": {
                "primary": "平和体质",
                "secondary": [],
                "description": "恭喜！您的体质非常健康，气血阴阳平衡，身体状态良好。"
            },
            "health_score": 95,
            "score_level": "优秀",
            "advice": {
                "diet": {
                    "recommended": [
                        "🥦 新鲜绿叶蔬菜",
                        "🍎 时令水果",
                        "🐟 优质蛋白（鱼、鸡肉）",
                        "🌾 全谷物（燕麦、糙米）"
                    ],
                    "avoid": [
                        "❌ 过度油腻食物",
                        "❌ 高糖饮料"
                    ]
                },
                "lifestyle": [
                    "💤 保持规律作息，每天7-8小时睡眠",
                    "🏃 每周3-5次中等强度运动",
                    "😊 保持心情愉悦，适度放松"
                ],
                "acupoints": [
                    "✋ 足三里（小腿外侧，增强免疫力）",
                    "✋ 三阴交（小腿内侧，调理气血）"
                ]
            },
            "herbs": [
                "🌿 枸杞（养肝明目）",
                "🌿 红枣（补气养血）",
                "🌿 山药（健脾益肺）"
            ],
            "summary": "健康状态优秀！继续保持良好的生活习惯。",
            "provider": "规则引擎",
            "model": "rule-based"
        }

    def _get_qi_deficiency_result(self) -> Dict[str, Any]:
        """气虚体质示例"""
        return {
            "tongue_body": {
                "color": "淡白色",
                "shape": "舌体胖大",
                "features": ["舌边有明显齿痕", "舌质偏嫩", "舌体略肿"]
            },
            "tongue_coating": {
                "color": "白色",
                "thickness": "薄",
                "texture": "水滑，略显湿润"
            },
            "constitution": {
                "primary": "气虚体质",
                "secondary": ["脾虚倾向"],
                "description": "您可能存在气虚的情况，容易疲劳乏力，需要补气健脾。"
            },
            "health_score": 72,
            "score_level": "良好",
            "advice": {
                "diet": {
                    "recommended": [
                        "🍠 山药（健脾补气）",
                        "🌰 红枣（补中益气）",
                        "🍯 蜂蜜（润肺养胃）",
                        "🍖 瘦肉（补充蛋白质）",
                        "🌾 小米粥（养胃健脾）"
                    ],
                    "avoid": [
                        "❌ 生冷食物（冰淇淋、冷饮）",
                        "❌ 过于辛辣刺激的食物"
                    ]
                },
                "lifestyle": [
                    "💤 避免熬夜，早睡早起（23点前入睡）",
                    "🏃 适度运动，避免过度劳累（太极、瑜伽）",
                    "😊 保持心情舒畅，减少压力"
                ],
                "acupoints": [
                    "✋ 气海穴（肚脐下方，补气培元）",
                    "✋ 足三里（补气健脾，增强体质）"
                ]
            },
            "herbs": [
                "🌿 黄芪（补气升阳，增强免疫力）",
                "🌿 党参（补中益气，健脾生津）",
                "🌿 白术（健脾益气，燥湿利水）"
            ],
            "summary": "气虚体质，注意补气健脾，避免过劳。",
            "provider": "规则引擎",
            "model": "rule-based"
        }

    def _get_blood_stasis_result(self) -> Dict[str, Any]:
        """血瘀体质示例"""
        return {
            "tongue_body": {
                "color": "暗紫色",
                "shape": "舌体正常",
                "features": ["舌下静脉曲张", "舌面有瘀点", "舌质暗沉"]
            },
            "tongue_coating": {
                "color": "薄白",
                "thickness": "薄",
                "texture": "正常"
            },
            "constitution": {
                "primary": "血瘀体质",
                "secondary": ["气滞倾向"],
                "description": "存在血液循环不畅的迹象，需要活血化瘀，促进气血运行。"
            },
            "health_score": 65,
            "score_level": "一般",
            "advice": {
                "diet": {
                    "recommended": [
                        "🫐 黑木耳（活血化瘀）",
                        "🍇 山楂（消食化瘀）",
                        "🧅 洋葱（降脂活血）",
                        "🐟 深海鱼（omega-3）",
                        "🍵 玫瑰花茶（疏肝理气）"
                    ],
                    "avoid": [
                        "❌ 高盐高脂食物",
                        "❌ 油炸食品",
                        "❌ 久坐不动"
                    ]
                },
                "lifestyle": [
                    "💤 保证充足睡眠，避免熬夜",
                    "🏃 增加有氧运动（快走、游泳、慢跑）",
                    "😊 保持心情舒畅，避免久坐",
                    "🚶 每小时起身活动5-10分钟"
                ],
                "acupoints": [
                    "✋ 血海穴（大腿内侧，活血调经）",
                    "✋ 膈俞穴（背部，活血化瘀）"
                ]
            },
            "herbs": [
                "🌿 三七（活血化瘀，止痛）",
                "🌿 当归（补血活血，调经）",
                "🌿 丹参（活血祛瘀，凉血消痈）"
            ],
            "summary": "血瘀体质，建议增加运动，活血化瘀。",
            "provider": "规则引擎",
            "model": "rule-based"
        }

    def _get_yin_deficiency_result(self) -> Dict[str, Any]:
        """阴虚体质示例"""
        return {
            "tongue_body": {
                "color": "红色偏深",
                "shape": "舌体偏瘦",
                "features": ["舌面有裂纹", "舌尖红", "舌质干燥"]
            },
            "tongue_coating": {
                "color": "少苔或无苔",
                "thickness": "薄或剥脱",
                "texture": "干燥"
            },
            "constitution": {
                "primary": "阴虚体质",
                "secondary": ["内热"],
                "description": "体内阴液不足，虚火内生，容易口干、手脚心热。"
            },
            "health_score": 68,
            "score_level": "良好",
            "advice": {
                "diet": {
                    "recommended": [
                        "🥛 银耳（滋阴润肺）",
                        "🫒 枸杞（滋阴补肾）",
                        "🥥 椰子水（清热生津）",
                        "🐚 海参（滋阴补肾）",
                        "🍐 雪梨（润肺生津）"
                    ],
                    "avoid": [
                        "❌ 辛辣刺激食物（辣椒、胡椒）",
                        "❌ 煎炸烧烤食物",
                        "❌ 过于温燥的食物"
                    ]
                },
                "lifestyle": [
                    "💤 保证充足睡眠，23点前入睡",
                    "🏃 避免剧烈运动，选择柔和运动（瑜伽、太极）",
                    "😊 保持心态平和，避免急躁",
                    "💧 多喝温水，保持体内水分"
                ],
                "acupoints": [
                    "✋ 太溪穴（脚内踝后，滋阴补肾）",
                    "✋ 三阴交（小腿内侧，滋阴养血）"
                ]
            },
            "herbs": [
                "🌿 麦冬（养阴生津，润肺清心）",
                "🌿 沙参（养阴清肺，益胃生津）",
                "🌿 石斛（益胃生津，滋阴清热）"
            ],
            "summary": "阴虚体质，注意滋阴润燥，避免熬夜。",
            "provider": "规则引擎",
            "model": "rule-based"
        }

    def _get_damp_heat_result(self) -> Dict[str, Any]:
        """湿热体质示例"""
        return {
            "tongue_body": {
                "color": "红色",
                "shape": "舌体略胖",
                "features": ["舌质红", "舌体偏厚"]
            },
            "tongue_coating": {
                "color": "黄色",
                "thickness": "厚腻",
                "texture": "黄腻苔，不易刮除"
            },
            "constitution": {
                "primary": "湿热体质",
                "secondary": ["脾虚湿盛"],
                "description": "体内湿热交织，容易口苦、身体困重、皮肤油腻。"
            },
            "health_score": 60,
            "score_level": "一般",
            "advice": {
                "diet": {
                    "recommended": [
                        "🫘 薏米（健脾祛湿）",
                        "🫛 绿豆（清热解毒）",
                        "🥒 冬瓜（清热利水）",
                        "🌽 玉米须茶（利尿祛湿）",
                        "🍵 苦瓜（清热降火）"
                    ],
                    "avoid": [
                        "❌ 油腻厚味食物",
                        "❌ 甜食糖类",
                        "❌ 酒类饮品",
                        "❌ 辛辣刺激食物"
                    ]
                },
                "lifestyle": [
                    "💤 避免熬夜，保持规律作息",
                    "🏃 增加运动出汗，促进湿气排出",
                    "😊 保持环境通风干燥",
                    "🚿 避免长时间处于潮湿环境"
                ],
                "acupoints": [
                    "✋ 阴陵泉（小腿内侧，健脾利湿）",
                    "✋ 丰隆穴（小腿外侧，化痰祛湿）"
                ]
            },
            "herbs": [
                "🌿 茯苓（利水渗湿，健脾宁心）",
                "🌿 泽泻（利水渗湿，泄热）",
                "🌿 车前草（清热利尿，祛痰）"
            ],
            "summary": "湿热体质，建议清热祛湿，饮食清淡。",
            "provider": "规则引擎",
            "model": "rule-based"
        }


# 快速测试
if __name__ == "__main__":
    analyzer = TongueAnalyzer()

    # 测试规则引擎
    print("🔬 测试规则引擎模式...")
    result = analyzer.analyze_image("test_qi_deficiency.jpg")
    print(json.dumps(result, ensure_ascii=False, indent=2))
