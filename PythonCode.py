from flask import Flask, request, jsonify
from huggingface_hub import InferenceClient
import os

app = Flask(__name__)
HUGGINGFACE_API_TOKEN = os.getenv("meow")  # مفتاح البسبس 🐾
HF_MODEL = "tiiuae/falcon-7b-instruct"     # ✅ النموذج الجديد

client = InferenceClient(token=HUGGINGFACE_API_TOKEN)

def get_huggingface_reply(user_text):
    prompt = f"اقترح ردين يعبرون عن رغبة المستخدم فقط، باللهجة الخليجية أو العربية البسيطة. النص: {user_text}"
    try:
        response = client.text_generation(prompt, model=HF_MODEL, max_new_tokens=100)
        print("📥 Raw Response:", response)
        replies = [line.strip("-• ").strip() for line in response.split("\n") if line.strip()]
        print("📤 الرد الجاهز:", replies)
        return replies[:2]
    except Exception as e:
        print("❌ Hugging Face Error:", str(e))
        return [f"❌ Error: {str(e)}", ""]

@app.route('/api', methods=['POST'])
def receive_text():
    print("📥 تم استقبال طلب من Arduino")
    data = request.get_json()
    user_text = data.get("text", "")
    print("📝 النص المستلم:", user_text)

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
    print("✅ تم الوصول إلى الصفحة الرئيسية من Arduino أو المتصفح")
    return "✅ السيرفر شغّال وجاهز لاستقبال الطلبات"
