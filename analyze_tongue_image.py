#!/usr/bin/env python3
"""
舌象分析工具 - 用于分析单张舌象图片
"""

import sys
import json
from tongue_feature_extractor import TongueFeatureExtractor

def analyze_tongue(image_path: str):
    """分析舌象图片并输出详细报告"""

    print("=" * 60)
    print("🔬 舌象智能分析系统")
    print("=" * 60)
    print(f"\n📸 正在分析图片: {image_path}\n")

    try:
        # 初始化特征提取器
        extractor = TongueFeatureExtractor()

        # 提取特征
        print("🔍 正在提取舌象特征...\n")
        features = extractor.extract_features(image_path)

        # 显示分析结果
        print("=" * 60)
        print("📊 分析结果")
        print("=" * 60)

        # 1. 舌质颜色
        print(f"\n🎨 【舌质颜色】")
        print(f"   类型: {features['tongue_color']['type']}")
        print(f"   描述: {features['tongue_color']['description']}")
        print(f"   色调值: {features['tongue_color']['hue']:.1f}")
        print(f"   饱和度: {features['tongue_color']['saturation']:.1f}")
        print(f"   亮度值: {features['tongue_color']['brightness']:.1f}")

        # 2. 舌苔特征
        print(f"\n📏 【舌苔特征】")
        print(f"   厚薄: {features['coating']['thickness']}")
        print(f"   颜色: {features['coating']['color']}")
        print(f"   描述: {features['coating']['description']}")
        print(f"   纹理复杂度: {features['coating']['edge_density']:.3f}")
        print(f"   纹理方差: {features['coating']['texture_variance']:.2f}")

        # 3. 舌形特征
        print(f"\n🔷 【舌形特征】")
        print(f"   类型: {features['shape']['type']}")
        print(f"   圆度: {features['shape']['circularity']:.3f}")
        print(f"   描述: {features['shape']['description']}")

        # 4. 舌面纹理
        print(f"\n✨ 【舌面纹理】")
        print(f"   纹理复杂度: {features['texture']['complexity']:.2f}")
        print(f"   是否有齿痕: {'是' if features['texture']['has_teeth_marks'] else '否'}")
        print(f"   特征: {', '.join(features['texture']['features'])}")
        print(f"   描述: {features['texture']['description']}")

        # 5. 综合评估
        print(f"\n📋 【综合评估】")
        print(f"   {features['summary']}")

        # 6. 健康提示
        print(f"\n⚠️  【健康提示】")
        analyze_health_issues(features)

        print("\n" + "=" * 60)
        print("✅ 分析完成")
        print("=" * 60)

        # 保存JSON结果
        output_file = image_path.rsplit('.', 1)[0] + '_analysis.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(features, f, ensure_ascii=False, indent=2)
        print(f"\n💾 详细结果已保存到: {output_file}")

    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()

def analyze_health_issues(features):
    """根据特征分析可能的健康问题"""

    issues = []

    # 分析舌质颜色
    color_type = features['tongue_color']['type']
    if color_type == "淡白舌":
        issues.append("⚠️  舌色偏淡，可能提示气血不足、阳虚体质")
        issues.append("   建议：多吃补气血的食物（红枣、桂圆、牛肉等）")
    elif color_type == "红舌":
        issues.append("⚠️  舌色偏红，可能有热证或阴虚")
        issues.append("   建议：注意清热降火，避免辛辣刺激食物")
    elif color_type == "绛舌":
        issues.append("⚠️  舌色深红，热证较重")
        issues.append("   建议：及时就医，可能需要清热治疗")
    elif color_type == "紫舌":
        issues.append("⚠️  舌色青紫，可能有血瘀或寒证")
        issues.append("   建议：注意活血化瘀，保持血液循环")

    # 分析舌苔
    coating = features['coating']['thickness']
    if "厚苔" in coating:
        issues.append("⚠️  舌苔较厚，可能提示消化不良或湿气重")
        issues.append("   建议：饮食清淡，减少油腻食物，适当运动")

    coating_color = features['coating']['color']
    if "黄苔" in coating_color:
        issues.append("⚠️  舌苔发黄，可能有热证或湿热")
        issues.append("   建议：清热祛湿，多喝水，避免熬夜")

    # 分析齿痕
    if features['texture']['has_teeth_marks']:
        issues.append("⚠️  有齿痕印迹，可能提示脾虚、气虚或湿气重")
        issues.append("   建议：健脾益气，注意休息，避免过度疲劳")

    # 输出问题
    if issues:
        for issue in issues:
            print(f"   {issue}")
    else:
        print("   ✅ 舌象特征正常，继续保持良好的生活习惯！")

    print(f"\n   ℹ️  注意：此分析仅供参考，不能替代专业医生诊断。")
    print(f"   ℹ️  如有持续不适，请及时就医咨询专业中医师。")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 analyze_tongue_image.py <图片路径>")
        print("示例: python3 analyze_tongue_image.py test_images/tongue.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    analyze_tongue(image_path)
