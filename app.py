"""
AI舌象分析Demo Web应用
支持图片上传、AI分析、动画展示
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import base64
from datetime import datetime
from analyzer import TongueAnalyzer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads/tongues'

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化分析器（如果没有API密钥，会自动使用规则引擎）
analyzer = TongueAnalyzer()


@app.route('/')
def index():
    """首页 - 舌象分析入口"""
    return render_template('tongue_demo/index.html')


@app.route('/demo')
def demo():
    """演示页面 - 典型舌象案例"""
    typical_cases = [
        {
            'id': 'healthy',
            'name': '🌕 健康星球',
            'emoji': '😊',
            'description': '舌质淡红，舌苔薄白 · 完美的健康状态',
            'score': 95,
            'color': '#4CAF50',
            'population': '2.3万',
            'stories': '1,234'
        },
        {
            'id': 'qi_deficiency',
            'name': '🪐 气虚星球',
            'emoji': '😮‍💨',
            'description': '舌体胖大，舌边齿痕 · 需要补气健脾',
            'score': 72,
            'color': '#FFC107',
            'population': '15.7万',
            'stories': '8,901'
        },
        {
            'id': 'blood_stasis',
            'name': '🔴 血瘀星球',
            'emoji': '😰',
            'description': '舌质暗紫，有瘀点 · 活血化瘀进行中',
            'score': 65,
            'color': '#FF5722',
            'population': '8.9万',
            'stories': '5,678'
        },
        {
            'id': 'yin_deficiency',
            'name': '🌙 阴虚星球',
            'emoji': '🥵',
            'description': '舌红少苔，有裂纹 · 滋阴润燥社区',
            'score': 68,
            'color': '#FF9800',
            'population': '11.2万',
            'stories': '6,543'
        },
        {
            'id': 'damp_heat',
            'name': '🌑 湿热星球',
            'emoji': '😓',
            'description': '舌苔黄腻，舌质红 · 清热祛湿互助组',
            'score': 60,
            'color': '#F44336',
            'population': '12.1万',
            'stories': '9,876'
        }
    ]
    return render_template('tongue_demo/demo.html', cases=typical_cases)


@app.route('/api/analyze', methods=['POST'])
def analyze_tongue():
    """
    API: 分析上传的舌象图片
    """
    if 'tongue_image' not in request.files:
        return jsonify({'success': False, 'error': '未上传图片'}), 400

    file = request.files['tongue_image']

    if file.filename == '':
        return jsonify({'success': False, 'error': '未选择文件'}), 400

    # 检查文件类型
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    if not ('.' in file.filename and
            file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return jsonify({'success': False, 'error': '不支持的文件格式'}), 400

    try:
        # 保存上传的文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"tongue_{timestamp}.{file.filename.rsplit('.', 1)[1].lower()}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # AI分析
        result = analyzer.analyze_image(filepath)

        # 添加图片URL（用于显示）
        with open(filepath, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
            result['image_url'] = f"data:image/jpeg;base64,{img_data}"

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/demo-analyze/<case_id>')
def demo_analyze(case_id):
    """
    API: 分析典型案例（用于演示）
    """
    try:
        # 使用规则引擎生成对应的分析结果
        fake_path = f"demo_{case_id}.jpg"
        result = analyzer.analyze_image(fake_path)

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/report')
def report():
    """报告页面"""
    return render_template('tongue_demo/report.html')


@app.route('/about')
def about():
    """关于页面"""
    return render_template('tongue_demo/about.html')


# 静态文件服务（用于开发）
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    print("=" * 60)
    print("🔬 AI舌象分析Demo启动中...")
    print("=" * 60)
    print(f"📊 分析引擎: {analyzer.provider if not analyzer.use_mock else '规则引擎'}")
    print(f"🌐 访问地址: http://localhost:5001")
    print(f"📁 上传目录: {app.config['UPLOAD_FOLDER']}")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5001)
