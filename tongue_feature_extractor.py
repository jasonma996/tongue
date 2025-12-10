"""
舌象图像特征提取器
使用 OpenCV 提取舌质颜色、舌苔特征、舌形等信息
"""

import cv2
import numpy as np
from typing import Dict, Any, Tuple, List


class TongueFeatureExtractor:
    """舌象特征提取器"""

    def __init__(self):
        """初始化特征提取器"""
        pass

    def extract_features(self, image_path: str) -> Dict[str, Any]:
        """
        提取舌象图片的所有特征

        Args:
            image_path: 图片路径

        Returns:
            特征字典
        """
        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法读取图片: {image_path}")

        # 提取各项特征
        tongue_color = self._analyze_tongue_color(image)
        coating_features = self._analyze_coating(image)
        shape_features = self._analyze_shape(image)
        texture_features = self._analyze_texture(image)

        return {
            "tongue_color": tongue_color,
            "coating": coating_features,
            "shape": shape_features,
            "texture": texture_features,
            "summary": self._generate_summary(
                tongue_color, coating_features, shape_features, texture_features
            )
        }

    def _analyze_tongue_color(self, image: np.ndarray) -> Dict[str, Any]:
        """
        分析舌质颜色

        Returns:
            舌质颜色特征
        """
        # 转换到 HSV 色彩空间
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 获取中心区域（避免边缘影响）
        h, w = image.shape[:2]
        center_region = hsv[h//4:3*h//4, w//4:3*w//4]

        # 计算平均色调、饱和度、亮度
        avg_h = np.mean(center_region[:, :, 0])
        avg_s = np.mean(center_region[:, :, 1])
        avg_v = np.mean(center_region[:, :, 2])

        # 判断舌质颜色类型
        color_type = self._classify_tongue_color(avg_h, avg_s, avg_v)

        return {
            "type": color_type,
            "hue": float(avg_h),
            "saturation": float(avg_s),
            "brightness": float(avg_v),
            "description": self._describe_color(color_type)
        }

    def _classify_tongue_color(self, h: float, s: float, v: float) -> str:
        """
        根据 HSV 值分类舌质颜色

        中医舌诊颜色分类：
        - 淡白舌：低饱和度，高亮度
        - 淡红舌（正常）：中等饱和度，中高亮度
        - 红舌：较高饱和度，中亮度
        - 绛舌：高饱和度，低中亮度
        - 紫舌：偏蓝色调
        """
        if v > 180 and s < 60:
            return "淡白舌"
        elif h < 20 and s > 100 and v < 150:
            return "绛舌"
        elif h < 15 and s > 70:
            return "红舌"
        elif h > 120 and h < 150:
            return "紫舌"
        else:
            return "淡红舌"

    def _describe_color(self, color_type: str) -> str:
        """生成颜色描述"""
        descriptions = {
            "淡白舌": "舌色较淡，可能气血不足",
            "淡红舌": "舌色淡红润泽，属于健康舌象",
            "红舌": "舌色偏红，可能有热证",
            "绛舌": "舌色深红，提示热盛",
            "紫舌": "舌色青紫，可能有血瘀"
        }
        return descriptions.get(color_type, "舌色正常")

    def _analyze_coating(self, image: np.ndarray) -> Dict[str, Any]:
        """
        分析舌苔特征

        Returns:
            舌苔特征
        """
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 获取中心区域
        h, w = gray.shape
        center = gray[h//4:3*h//4, w//4:3*w//4]

        # 计算纹理复杂度（舌苔厚薄的指标）
        edges = cv2.Canny(center, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size

        # 计算亮度标准差（舌苔厚薄的另一指标）
        std_dev = np.std(center)

        # 判断舌苔厚薄
        if edge_density > 0.15 or std_dev > 40:
            thickness = "厚苔"
        elif edge_density < 0.05 and std_dev < 20:
            thickness = "薄苔"
        else:
            thickness = "薄白苔"

        # 判断舌苔颜色（通过亮度判断）
        avg_brightness = np.mean(center)
        if avg_brightness > 150:
            coating_color = "白苔"
        elif avg_brightness > 100:
            coating_color = "淡黄苔"
        else:
            coating_color = "黄苔"

        return {
            "thickness": thickness,
            "color": coating_color,
            "edge_density": float(edge_density),
            "texture_variance": float(std_dev),
            "description": self._describe_coating(thickness, coating_color)
        }

    def _describe_coating(self, thickness: str, color: str) -> str:
        """生成舌苔描述"""
        return f"{color}，{thickness}"

    def _analyze_shape(self, image: np.ndarray) -> Dict[str, Any]:
        """
        分析舌形特征

        Returns:
            舌形特征
        """
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 边缘检测
        edges = cv2.Canny(gray, 50, 150)

        # 查找轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return {
                "type": "正常舌形",
                "description": "舌形大小适中"
            }

        # 获取最大轮廓（假设为舌头）
        largest_contour = max(contours, key=cv2.contourArea)

        # 计算轮廓面积和周长
        area = cv2.contourArea(largest_contour)
        perimeter = cv2.arcLength(largest_contour, True)

        # 计算圆度（判断舌形是否规则）
        if perimeter > 0:
            circularity = 4 * np.pi * area / (perimeter ** 2)
        else:
            circularity = 0

        # 判断舌形类型
        if circularity > 0.8:
            shape_type = "舌体圆润"
        elif circularity < 0.6:
            shape_type = "舌体瘦长"
        else:
            shape_type = "舌形正常"

        return {
            "type": shape_type,
            "circularity": float(circularity),
            "area": float(area),
            "description": shape_type
        }

    def _analyze_texture(self, image: np.ndarray) -> Dict[str, Any]:
        """
        分析舌面纹理（齿痕、裂纹等）

        Returns:
            纹理特征
        """
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 使用 Laplacian 算子检测纹理复杂度
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        texture_complexity = np.var(laplacian)

        # 判断是否有齿痕或裂纹
        if texture_complexity > 200:
            features = ["明显纹理", "可能有齿痕或裂纹"]
            has_teeth_marks = True
        elif texture_complexity > 100:
            features = ["轻微纹理"]
            has_teeth_marks = False
        else:
            features = ["表面光滑"]
            has_teeth_marks = False

        return {
            "complexity": float(texture_complexity),
            "has_teeth_marks": has_teeth_marks,
            "features": features,
            "description": "、".join(features)
        }

    def _generate_summary(
        self,
        tongue_color: Dict,
        coating: Dict,
        shape: Dict,
        texture: Dict
    ) -> str:
        """
        生成特征总结

        Returns:
            特征总结文字
        """
        summary_parts = [
            f"舌质：{tongue_color['type']}",
            f"舌苔：{coating['description']}",
            f"舌形：{shape['description']}",
            f"舌面：{texture['description']}"
        ]

        return "；".join(summary_parts)


# 测试函数
if __name__ == "__main__":
    extractor = TongueFeatureExtractor()

    # 测试示例
    test_image = "uploads/tongues/test.jpg"
    if os.path.exists(test_image):
        features = extractor.extract_features(test_image)
        print("提取的特征：")
        print(json.dumps(features, ensure_ascii=False, indent=2))
