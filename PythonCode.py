from flask import Flask, request, jsonify
from huggingface_hub import InferenceClient
import os

app = Flask(__name__)
HUGGINGFACE_API_TOKEN = os.getenv("meow")  # مفتاح البسبس 🐾
HF_MODEL = "google/flan-t5-base"

# إنشاء العميل
client = InferenceClient(token=HUGGINGFACE_API_TOKEN)

def get_huggingface_reply(user_text):
    prompt = f"اقترح ردين يعبرون عن رغبة المستخدم فقط، باللهجة الخليجية أو العربية البسيطة. النص: {user_text}"
    try:
        response = client.text_generation(prompt, model=HF_MODEL, max_new_tokens=100)
        replies = [line.strip("-• ").strip() for line in response.split("\n") if line.strip()]
        return replies[:2]
    except Exception as e:
        print("❌ Hugging Face Error:", str(e))
        return [f"❌ Error: {str(e)}", ""]

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
