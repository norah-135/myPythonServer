from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
HUGGINGFACE_API_TOKEN = os.getenv("meow")  # مفتاح البسبس 🐾
HF_MODEL = "google/flan-t5-base"

def get_huggingface_reply(user_text):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    payload = {
        "inputs": f"اقترح ردين يعبرون عن رغبة المستخدم فقط، باللهجة الخليجية أو العربية البسيطة. النص: {user_text}",
        "parameters": {"max_new_tokens": 100}
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        result = response.json()
        text = result[0]["generated_text"]
        replies = [line.strip("-• ").strip() for line in text.split("\n") if line.strip()]
        return replies[:2]
    else:
        print("❌ Hugging Face Error:", response.text)
        return [f"❌ Error {response.status_code}", ""]

@app.route('/api', methods=['POST'])
def receive_text():
    data = request.get_json()
    user_text = data.get("text", "")

    try:
        replies = get_huggingface_reply(user_text)

        return jsonify({
            "reply_1": replies[0] if len(replies) > 0 else "",
            "reply_2": replies[1] if len(replies) > 1 else ""
        })

    except Exception as e:
        print("❌ Server Error:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "✅ السيرفر شغّال"
