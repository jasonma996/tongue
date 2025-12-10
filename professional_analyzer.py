"""
专业舌象分析器 - 使用 Claude Vision 或 GPT-4 Vision
提供医学级别的准确分析
"""

import os
import json
import base64
from typing import Dict, Any

class ProfessionalTongueAnalyzer:
    """专业级舌象分析器 - 使用视觉AI模型"""

    def __init__(self, provider: str = "claude"):
        """
        初始化专业分析器

        Args:
            provider: 'claude' 或 'gpt4' 或 'gemini'
        """
        self.provider = provider

        if provider == "claude":
            self.api_key = os.getenv('ANTHROPIC_API_KEY')
            if not self.api_key:
                raise ValueError("请设置 ANTHROPIC_API_KEY 环境变量")
        elif provider == "gpt4":
            self.api_key = os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError("请设置 OPENAI_API_KEY 环境变量")
        elif provider == "gemini":
            self.api_key = os.getenv('GOOGLE_API_KEY')
            if not self.api_key:
                raise ValueError("请设置 GOOGLE_API_KEY 环境变量")

        self._init_client()

    def _init_client(self):
        """初始化AI客户端"""
        if self.provider == "claude":
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
            print("✅ Claude Vision 客户端初始化成功 (专业模式)")

        elif self.provider == "gpt4":
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            print("✅ GPT-4 Vision 客户端初始化成功 (专业模式)")

        elif self.provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai
            print("✅ Gemini Vision 客户端初始化成功 (专业模式)")

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        专业级舌象分析

        Args:
            image_path: 图片路径

        Returns:
            详细的医学分析结果
        """
        print(f"\n🔬 使用 {self.provider.upper()} 进行专业级舌象分析...")

        if self.provider == "claude":
            return self._analyze_with_claude(image_path)
        elif self.provider == "gpt4":
            return self._analyze_with_gpt4(image_path)
        elif self.provider == "gemini":
            return self._analyze_with_gemini(image_path)

    def _analyze_with_claude(self, image_path: str) -> Dict[str, Any]:
        """使用 Claude 3.5 Sonnet Vision 分析（最推荐）"""

        # 读取并编码图片
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        # 确定图片格式
        if image_path.lower().endswith('.png'):
            media_type = "image/png"
        elif image_path.lower().endswith('.webp'):
            media_type = "image/webp"
        else:
            media_type = "image/jpeg"

        # 专业中医舌诊提示词
        prompt = """你是一位具有30年经验的中医舌诊专家。请从专业医学角度详细分析这张舌象照片。

【专业分析要求】

1. **舌体分析**（Tongue Body）：
   - 舌色：淡白/淡红/红/绛红/青紫？准确判断
   - 舌形：老嫩、胖瘦、点刺、裂纹、齿痕的具体位置和程度
   - 舌态：是否歪斜、颤动、强硬、痿软

2. **舌苔分析**（Tongue Coating）：
   - 苔色：白/黄/灰/黑？准确判断
   - 苔质：厚薄、腐腻、润燥的具体程度
   - 苔的分布：全舌/舌根/舌中/舌边等部位差异

3. **中医辨证**（TCM Diagnosis）：
   - 体质类型：9种体质精确判断（平和/气虚/阳虚/阴虚/痰湿/湿热/血瘀/气郁/特禀）
   - 病理性质：寒/热/虚/实/表/里
   - 病位：心/肝/脾/肺/肾等脏腑
   - 病程：急性/慢性/病情轻重

4. **医学评估**：
   - 健康评分（0-100分）
   - 需要关注的问题（按重要性排序）
   - 是否需要就医（紧急/建议/暂不需要）

5. **专业建议**：
   - 饮食调理（具体食材和做法）
   - 生活起居（作息、运动、情志）
   - 中药方剂（经典方剂建议）
   - 穴位按摩（具体穴位和手法）

【输出格式 - 严格JSON】
{
  "tongue_body": {
    "color": "具体舌色",
    "color_description": "详细描述（50字）",
    "shape": "舌形特征",
    "shape_details": {
      "tenderness": "老/嫩",
      "size": "胖大/瘦小/适中",
      "teeth_marks": "有/无（位置）",
      "cracks": "有/无（类型）",
      "petechiae": "有/无（位置）"
    },
    "motion": "舌态描述"
  },
  "tongue_coating": {
    "color": "苔色",
    "color_description": "详细描述",
    "thickness": "厚/薄/适中",
    "texture": "腐/腻/润/燥",
    "texture_description": "详细描述",
    "distribution": "全舌/根部/中部等",
    "coverage": "全覆盖/部分剥脱等"
  },
  "tcm_diagnosis": {
    "constitution": {
      "primary": "主要体质",
      "secondary": ["次要体质"],
      "confidence": "置信度0-100%",
      "description": "体质详细说明（100字）"
    },
    "pathology": {
      "nature": ["寒/热/虚/实"],
      "location": ["病位脏腑"],
      "severity": "轻度/中度/重度",
      "duration": "急性/慢性"
    },
    "syndrome": "中医证型（如：脾胃虚寒证）"
  },
  "health_assessment": {
    "score": 数字0-100,
    "level": "优秀/良好/一般/较差/很差",
    "concerns": [
      {
        "issue": "问题描述",
        "severity": "轻度/中度/重度",
        "recommendation": "处理建议"
      }
    ],
    "medical_attention": "不需要/建议就医/尽快就医/紧急就医",
    "medical_reason": "就医建议的理由"
  },
  "advice": {
    "diet": {
      "principles": ["饮食原则1", "原则2"],
      "recommended": [
        {
          "food": "食物名称",
          "reason": "推荐理由",
          "method": "烹饪方法"
        }
      ],
      "avoid": [
        {
          "food": "食物名称",
          "reason": "避免原因"
        }
      ],
      "recipes": [
        {
          "name": "食疗方名称",
          "ingredients": ["材料1", "材料2"],
          "method": "制作方法",
          "effect": "功效"
        }
      ]
    },
    "lifestyle": {
      "sleep": "睡眠建议",
      "exercise": "运动建议",
      "emotion": "情志调理建议",
      "environment": "环境建议"
    },
    "herbal_formula": {
      "classic_formula": "经典方剂名称",
      "ingredients": ["药材1", "药材2"],
      "modification": "加减说明",
      "caution": "注意事项"
    },
    "acupoints": [
      {
        "name": "穴位名称",
        "location": "位置描述",
        "method": "按摩手法",
        "effect": "功效",
        "duration": "按摩时长"
      }
    ]
  },
  "summary": "一句话总结（30字内）",
  "detailed_analysis": "详细的专业分析报告（200-300字）",
  "disclaimer": "此分析仅供参考，不能替代专业医生诊断。如有不适，请及时就医。"
}

【注意事项】
1. 必须基于图片的实际特征进行分析，不要臆测
2. 如果某些特征不清晰，请在description中说明
3. 使用专业但通俗易懂的语言
4. 提供的建议必须安全、可操作
5. 强调不能替代医生诊断"""

        try:
            # 调用 Claude API
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                temperature=0.3,  # 降低temperature提高准确性
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )

            # 解析响应
            response_text = message.content[0].text

            # 提取JSON
            result = self._parse_json_response(response_text)
            result['provider'] = 'claude-vision'
            result['model'] = 'claude-3-5-sonnet'
            result['analysis_type'] = 'professional'

            print("✅ Claude Vision 专业分析完成")
            return result

        except Exception as e:
            print(f"❌ Claude API 调用失败: {e}")
            raise

    def _analyze_with_gpt4(self, image_path: str) -> Dict[str, Any]:
        """使用 GPT-4 Vision 分析"""
        # GPT-4 Vision 实现类似，使用 OpenAI API
        print("⚠️  GPT-4 Vision 分析暂未实现，请使用 Claude")
        raise NotImplementedError("请使用 provider='claude'")

    def _analyze_with_gemini(self, image_path: str) -> Dict[str, Any]:
        """使用 Gemini Vision 分析"""
        print("⚠️  Gemini Vision 分析暂未实现，请使用 Claude")
        raise NotImplementedError("请使用 provider='claude'")

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

        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            return {
                'error': 'JSON解析失败',
                'raw_response': response
            }


# 快速测试函数
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python3 professional_analyzer.py <图片路径>")
        print("示例: python3 professional_analyzer.py test_images/tongue.jpg")
        print("\n确保已设置环境变量: ANTHROPIC_API_KEY")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        analyzer = ProfessionalTongueAnalyzer(provider="claude")
        result = analyzer.analyze_image(image_path)

        print("\n" + "="*60)
        print("📊 专业分析结果")
        print("="*60)
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # 保存结果
        output_file = image_path.rsplit('.', 1)[0] + '_professional_analysis.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n💾 结果已保存到: {output_file}")

    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
