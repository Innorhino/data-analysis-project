from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 替换为您的 Google Chat Webhook URL
WEBHOOK = 'https://chat.googleapis.com/v1/spaces/AAAA60KHhTs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=G-mZEz98Q-wywBK4NP8aNXOuhKY_RBAcc-ThZNghuhw'
GPT_API_KEY = 'AIzaSyA_zQOXl3AiK93ckHY2Rz3ItYkwI6O4zDU'


@app.route('/')
def home():
    return "Flask app is running. Use /chat for Google Chat integration."


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    # 解析图片的 URL
    image_url = data['message']['attachments'][0]['imageUrl']

    # 处理图片并获取分析结果
    analysis_result = analyze_image(image_url)

    # 调用 GPT 模型
    gpt_result = call_gpt(analysis_result)

    # 发送结果回 Google Chat
    send_to_chat(gpt_result)

    return jsonify({"status": "success"}), 200


def analyze_image(image_url):
    # 在这里处理图片并返回尺寸和特殊工艺的描述
    return "尺寸: 10cm x 5cm; 特殊工艺: 手工雕刻"


def call_gpt(analysis_result):
    headers = {
        'Authorization': f'Bearer {GPT_API_KEY}',
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
    requests.post(WEBHOOK, json=payload)


if __name__ == '__main__':
    app.run(port=5000)
