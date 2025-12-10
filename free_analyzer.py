#!/usr/bin/env python3
"""
100% 免费舌象分析器
使用智谱AI GLM-4V（有免费额度）
"""

import os
import json
import base64
from typing import Dict, Any

class FreeTongueAnalyzer:
    """免费舌象分析器 - 使用智谱AI GLM-4V"""

    def __init__(self):
        """初始化免费分析器"""
        self.api_key = os.getenv('ZHIPU_API_KEY') or os.getenv('GLM_API_KEY')

        if not self.api_key:
            raise ValueError("""
❌ 请先设置API密钥！

获取免费API密钥步骤：
1. 访问：https://open.bigmodel.cn/
2. 注册账号（手机号即可）
3. 实名认证（中国身份证）
4. 获取API密钥（新用户送18元体验金）
5. 设置环境变量：
   export ZHIPU_API_KEY=your_api_key_here
            """)

        self._init_client()

    def _init_client(self):
        """初始化智谱AI客户端"""
        try:
            from zhipuai import ZhipuAI
            self.client = ZhipuAI(api_key=self.api_key)
            print("✅ 智谱AI GLM-4V 初始化成功（免费模式）")
            print("💰 使用免费额度，无需担心费用！")
        except ImportError:
            print("❌ 需要安装 zhipuai SDK")
            print("运行：pip install --break-system-packages zhipuai")
            raise

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        分析舌象图片（免费）

        Args:
            image_path: 图片路径

        Returns:
            详细的分析结果
        """
        print(f"\n🔬 使用智谱AI GLM-4V 免费分析舌象...")

        # 读取并编码图片
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        # 专业中医舌诊提示词
        prompt = """你是一位经验丰富的中医舌诊专家。请详细分析这张舌象照片，从中医角度给出专业评估。

【分析维度】
1. 舌体特征：
   - 舌色（淡白/淡红/红/绛红/青紫）
   - 舌形（老嫩、胖瘦、齿痕、裂纹）
   - 舌态（歪斜、颤动等）

2. 舌苔特征：
   - 苔色（白/黄/灰/黑）
   - 苔质（厚薄、腐腻、润燥）
   - 苔的分布（全舌/局部）

3. 中医辨证：
   - 体质类型（气虚/血瘀/阴虚/阳虚/湿热/痰湿/气郁/特禀/平和）
   - 病理性质（寒/热/虚/实）
   - 病位（心/肝/脾/肺/肾）

4. 健康建议：
   - 饮食调理（具体食物）
   - 生活建议（作息、运动）
   - 中药食疗（方剂建议）
   - 穴位按摩（具体穴位）

【输出格式 - 严格JSON】
{
  "tongue_body": {
    "color": "舌色",
    "color_description": "详细描述",
    "shape": "舌形特征",
    "teeth_marks": "有/无",
    "cracks": "有/无"
  },
  "tongue_coating": {
    "color": "苔色",
    "thickness": "厚/薄/适中",
    "texture": "腐/腻/润/燥",
    "distribution": "分布情况"
  },
  "constitution": {
    "primary": "主要体质",
    "secondary": ["次要体质"],
    "description": "体质说明（100字）"
  },
  "pathology": {
    "nature": ["寒/热/虚/实"],
    "location": ["脏腑"],
    "severity": "轻度/中度/重度"
  },
  "health_score": 数字0-100,
  "score_level": "优秀/良好/一般/较差",
  "advice": {
    "diet": {
      "recommended": [
        {"food": "食物名", "reason": "理由", "method": "做法"}
      ],
      "avoid": [
        {"food": "食物名", "reason": "理由"}
      ]
    },
    "lifestyle": {
      "sleep": "睡眠建议",
      "exercise": "运动建议",
      "emotion": "情志建议"
    },
    "herbal_formula": {
      "name": "方剂名称",
      "ingredients": ["药材"],
      "effect": "功效"
    },
    "acupoints": [
      {
        "name": "穴位名",
        "location": "位置",
        "method": "按摩手法",
        "effect": "功效"
      }
    ]
  },
  "summary": "一句话总结（30字内）",
  "disclaimer": "此分析仅供参考，不能替代医生诊断"
}

请基于图片实际特征分析，使用通俗易懂的语言，提供安全可操作的建议。"""

        try:
            # 调用智谱AI API (使用正确的格式)
            response = self.client.chat.completions.create(
                model="glm-4v-flash",  # 免费的视觉模型
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_data  # 直接使用base64字符串，不需要data:前缀
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )

            ai_response = response.choices[0].message.content

            # 解析JSON
            result = self._parse_json_response(ai_response)
            result['provider'] = 'zhipu-ai'
            result['model'] = 'glm-4v-flash'
            result['cost'] = '免费'

            print("✅ 智谱AI 免费分析完成！")
            print("💰 本次分析使用免费额度，无需付费")

            return result

        except Exception as e:
            print(f"❌ API调用失败: {e}")
            raise

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
            print(f"⚠️ JSON解析失败，返回原始文本")
            return {
                'raw_response': response,
                'note': '请查看raw_response字段获取完整分析'
            }

    def check_balance(self):
        """检查剩余免费额度"""
        # 智谱AI SDK可能没有直接的余额查询API
        # 用户可以登录控制台查看
        print("\n💰 查看剩余免费额度：")
        print("   访问：https://open.bigmodel.cn/usercenter/proj-mgmt/apikeys")
        print("   在控制台查看账户余额")


# 快速测试
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("""
🆓 免费舌象分析工具 - 智谱AI GLM-4V

用法：
  python3 free_analyzer.py <图片路径>

示例：
  python3 free_analyzer.py test_images/tongue.jpg

前置条件：
  1. 注册智谱AI账号：https://open.bigmodel.cn/
  2. 获取免费API密钥（新用户送18元）
  3. 设置环境变量：
     export ZHIPU_API_KEY=your_key_here
        """)
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        analyzer = FreeTongueAnalyzer()
        result = analyzer.analyze_image(image_path)

        print("\n" + "="*60)
        print("📊 免费分析结果")
        print("="*60)
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # 保存结果
        output_file = image_path.rsplit('.', 1)[0] + '_free_analysis.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n💾 结果已保存到: {output_file}")

        # 检查余额
        analyzer.check_balance()

    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
