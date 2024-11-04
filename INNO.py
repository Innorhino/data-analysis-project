from flask import Flask, request, jsonify
import requests
from PIL import Image
import io

app = Flask(__name__)

# 替换为您的 Google Chat Webhook URL（请确保这个 URL 和 Token 是有效的）
WEBHOOK = 'https://chat.googleapis.com/v1/spaces/AAAA60KHhTs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=G-mZEz98Q-wywBK4NP8aNXOuhKY_RBAcc-ThZNghuhw'
# 替换为你的有效 GPT API 密钥
GPT_API_KEY = 'AIzaSyCZqk89jWUd4EJ9ou37EVeiFJCx44FnxQU'


@app.route('/')
def home():
    return "Flask app is running. Use /upload to upload images."


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 将上传的图片文件转为 Image 对象
    image = Image.open(file.stream)

    # 处理图片并获取分析结果
    analysis_result = analyze_image(image)

    # 调用 GPT 模型
    gpt_result = call_gpt(analysis_result)

    # 发送结果回 Google Chat
    send_to_chat(gpt_result)

    return jsonify({"status": "success"}), 200


def analyze_image(image):
    # 这里可以根据需要对图片进行处理
    # 假设返回一个固定的描述，实际应用中可以加入更多逻辑
    return "尺寸: {} x {}; 特殊工艺: 手工雕刻".format(image.size[0], image.size[1])


def call_gpt(analysis_result):
    headers = {
        'Authorization': f'Bearer {GPT_API_KEY}',  # 确保你的 GPT API 密钥有效
        'Content-Type': 'application/json'
    }
    payload = {
        "prompt": f"分析结果: {analysis_result}",
        "max_tokens": 100
    }

    response = requests.post('https://api.gemini.example.com/v1/engines/gpt-4/completions', headers=headers,
                             json=payload)
    response_data = response.json()

    return response_data['choices'][0]['text']


def send_to_chat(message):
    payload = {
        "text": message
    }
    response = requests.post(WEBHOOK, json=payload)  # 检查 Webhook 的响应
    print(f'Sending to chat: {payload}, Response Code: {response.status_code}, Response: {response.text}')


if __name__ == '__main__':
    app.run(port=5000)
