#!/usr/bin/env python3
"""
AI Content Generator - Professional Health Platform
Uses GLM-4 to automatically generate professional health articles
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List
from zhipuai import ZhipuAI


class AIContentGenerator:
    """AI-powered content generator for professional health platform"""

    def __init__(self):
        """Initialize AI content generator"""
        self.api_key = os.getenv('ZHIPU_API_KEY') or os.getenv('GLM_API_KEY')

        if not self.api_key:
            raise ValueError("请设置 ZHIPU_API_KEY 环境变量")

        self.client = ZhipuAI(api_key=self.api_key)
        print("✅ AI Content Generator initialized with GLM-4")

    def generate_personalized_article(
        self,
        constitution: str,
        health_score: int,
        symptoms: List[str],
        health_goal: str = None
    ) -> Dict[str, Any]:
        """
        Generate personalized health article based on user data

        Args:
            constitution: User's TCM constitution type
            health_score: Health score (0-100)
            symptoms: List of symptoms
            health_goal: User's health goal (optional)

        Returns:
            Dict containing article title, content, category, tags, etc.
        """

        print(f"\n🤖 AI generating personalized article for {constitution}...")

        prompt = f"""你是一位专业的健康内容创作专家，拥有医学、营养学、心理学背景。

【用户画像】
- 体质类型：{constitution}
- 健康评分：{health_score}/100
- 主要症状：{', '.join(symptoms)}
{'- 健康目标：' + health_goal if health_goal else ''}

【任务】
请生成一篇专业的健康文章，帮助用户理解并改善自己的健康状况。

【文章要求】
1. 标题：吸引人且专业（20-30字）
2. 摘要：核心要点（50-80字）
3. 正文：结构清晰，分为4-5个部分
   - 第1部分：症状分析（为什么会出现这些问题）
   - 第2部分：深层原因（生理+心理+生活方式）
   - 第3部分：改善方案（具体可操作的建议）
   - 第4部分：成功案例（真实感的故事）
   - 第5部分：专家建议（专业但通俗易懂）
4. 字数：1500-2000字
5. 语言：专业但通俗易懂，避免过于学术化

【输出格式 - JSON】
{{
  "title": "文章标题",
  "subtitle": "副标题（可选）",
  "summary": "文章摘要",
  "category": "心理健康|职场健康|中医科普|改善故事",
  "tags": ["标签1", "标签2", "标签3"],
  "author": {{
    "name": "作者名（虚拟专家）",
    "title": "职称",
    "institution": "机构"
  }},
  "content": {{
    "section1": {{
      "title": "第一部分标题",
      "content": "内容..."
    }},
    "section2": {{
      "title": "第二部分标题",
      "content": "内容..."
    }},
    "section3": {{
      "title": "第三部分标题",
      "content": "内容..."
    }},
    "section4": {{
      "title": "第四部分标题",
      "content": "内容..."
    }},
    "section5": {{
      "title": "第五部分标题",
      "content": "内容..."
    }}
  }},
  "key_takeaways": [
    "关键要点1",
    "关键要点2",
    "关键要点3"
  ],
  "references": [
    "参考文献1（可以是虚拟的专业来源）",
    "参考文献2"
  ],
  "reading_time": "预计阅读时间（分钟）",
  "difficulty_level": "入门|中级|高级"
}}

【注意事项】
1. 内容必须专业、准确、有深度
2. 避免夸大或误导
3. 提供的建议必须安全、可操作
4. 语言要有同理心，理解用户的困扰
5. 加入真实感的细节和案例
"""

        try:
            # 调用 GLM-4 生成文章
            response = self.client.chat.completions.create(
                model="glm-4-flash",  # 使用 GLM-4 文本模型
                messages=[
                    {
                        "role": "system",
                        "content": "你是一位专业的健康内容创作专家，擅长将复杂的医学知识转化为通俗易懂的文章。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )

            ai_response = response.choices[0].message.content

            # 解析 JSON
            article = self._parse_json_response(ai_response)

            # 添加元数据
            article['generated_at'] = datetime.now().isoformat()
            article['generator'] = 'glm-4-flash'
            article['constitution_target'] = constitution
            article['health_score_target'] = health_score

            print("✅ Article generated successfully!")
            print(f"   Title: {article.get('title', 'N/A')}")
            print(f"   Category: {article.get('category', 'N/A')}")
            print(f"   Reading Time: {article.get('reading_time', 'N/A')}")

            return article

        except Exception as e:
            print(f"❌ Failed to generate article: {e}")
            raise

    def generate_health_encyclopedia_entry(self, topic: str) -> Dict[str, Any]:
        """
        Generate a health encyclopedia entry

        Args:
            topic: Health topic (e.g., "气虚体质", "失眠", "职场压力")

        Returns:
            Encyclopedia entry with definition, causes, symptoms, treatments
        """

        print(f"\n📚 AI generating encyclopedia entry for: {topic}")

        prompt = f"""你是一位医学百科编辑，请为"{topic}"创建一个专业的健康百科词条。

【词条要求】
1. 定义：简明扼要（50-100字）
2. 别名：其他常见叫法
3. 症状表现：列出主要症状（5-8个）
4. 成因分析：为什么会出现这个问题
5. 影响人群：哪些人容易出现
6. 诊断标准：如何判断（如果适用）
7. 治疗方法：
   - 中医治疗
   - 西医治疗
   - 饮食调理
   - 生活方式调整
8. 预防措施：如何避免
9. 常见误区：人们对这个问题的常见误解
10. 相关词条：关联的其他健康话题

【输出格式 - JSON】
{{
  "term": "{topic}",
  "definition": "定义",
  "aliases": ["别名1", "别名2"],
  "symptoms": ["症状1", "症状2"],
  "causes": {{
    "primary": ["主要原因1", "主要原因2"],
    "secondary": ["次要原因1", "次要原因2"]
  }},
  "affected_groups": ["人群1", "人群2"],
  "diagnosis": "诊断方法",
  "treatments": {{
    "tcm": ["中医方法1", "中医方法2"],
    "western": ["西医方法1", "西医方法2"],
    "diet": ["饮食建议1", "饮食建议2"],
    "lifestyle": ["生活方式1", "生活方式2"]
  }},
  "prevention": ["预防措施1", "预防措施2"],
  "misconceptions": [
    {{"myth": "误区1", "truth": "真相1"}},
    {{"myth": "误区2", "truth": "真相2"}}
  ],
  "related_terms": ["相关词条1", "相关词条2"],
  "severity": "轻度|中度|重度",
  "medical_attention": "是否需要就医"
}}
"""

        try:
            response = self.client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一位专业的医学百科编辑。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # 更低的temperature保证专业性
                max_tokens=3000
            )

            entry = self._parse_json_response(response.choices[0].message.content)
            entry['generated_at'] = datetime.now().isoformat()
            entry['generator'] = 'glm-4-flash'

            print(f"✅ Encyclopedia entry created: {topic}")
            return entry

        except Exception as e:
            print(f"❌ Failed to generate encyclopedia entry: {e}")
            raise

    def generate_weekly_health_tips(self, constitution_types: List[str]) -> List[Dict[str, Any]]:
        """
        Generate weekly health tips for different constitution types

        Args:
            constitution_types: List of constitution types to generate tips for

        Returns:
            List of health tips (one per day, 7 days)
        """

        print(f"\n💡 Generating weekly health tips for {len(constitution_types)} constitution types...")

        tips = []

        for constitution in constitution_types:
            prompt = f"""请为{constitution}的人群生成一周（7天）的健康小贴士。

每天的小贴士应该：
1. 简短实用（30-50字）
2. 可操作性强
3. 涵盖不同方面（饮食、运动、心理、睡眠等）

【输出格式 - JSON Array】
[
  {{
    "day": 1,
    "tip": "周一贴士内容",
    "category": "饮食|运动|心理|睡眠|其他"
  }},
  ...
]
"""

            try:
                response = self.client.chat.completions.create(
                    model="glm-4-flash",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000
                )

                daily_tips = self._parse_json_response(response.choices[0].message.content)

                for tip in daily_tips:
                    tip['constitution'] = constitution
                    tip['generated_at'] = datetime.now().isoformat()
                    tips.append(tip)

                print(f"  ✅ Generated 7 tips for {constitution}")

            except Exception as e:
                print(f"  ❌ Failed for {constitution}: {e}")
                continue

        return tips

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from AI response"""
        try:
            # 尝试提取 JSON 部分
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
            print(f"⚠️ JSON parsing failed: {e}")
            return {
                'error': 'JSON解析失败',
                'raw_response': response
            }


# Example usage and testing
if __name__ == "__main__":
    import sys

    generator = AIContentGenerator()

    print("\n" + "=" * 60)
    print("🤖 AI Content Generator - Professional Health Platform")
    print("=" * 60)

    # Example 1: Generate personalized article
    print("\n【示例 1】生成个性化健康文章")
    article = generator.generate_personalized_article(
        constitution="气虚质",
        health_score=68,
        symptoms=["疲劳", "气短", "免疫力低"],
        health_goal="3个月内改善体力，不再总是疲劳"
    )

    # Save article
    output_file = f"generated_article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Article saved to: {output_file}")

    # Example 2: Generate encyclopedia entry
    print("\n【示例 2】生成健康百科词条")
    entry = generator.generate_health_encyclopedia_entry("失眠")

    entry_file = f"encyclopedia_entry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(entry_file, 'w', encoding='utf-8') as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)

    print(f"💾 Encyclopedia entry saved to: {entry_file}")

    # Example 3: Generate weekly tips
    print("\n【示例 3】生成每周健康小贴士")
    tips = generator.generate_weekly_health_tips(["气虚质", "阴虚质"])

    tips_file = f"weekly_tips_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(tips_file, 'w', encoding='utf-8') as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

    print(f"💾 Weekly tips saved to: {tips_file}")
    print(f"   Total tips generated: {len(tips)}")

    print("\n" + "=" * 60)
    print("✅ AI Content Generation Complete!")
    print("=" * 60)
