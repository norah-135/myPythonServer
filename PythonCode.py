from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# مفتاح OpenAI من البيئة
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chatgpt_reply(user_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # أو gpt-4 إذا عندك صلاحية
            messages=[
                {"role": "system", "content": "أجب باللهجة الخليجية أو العربية البسيطة، واقترح ردين يعبرون عن رغبة المستخدم فقط"},
                {"role": "user", "content": user_text}
            ],
            max_tokens=100
        )
        full_text = response.choices[0].message.content
        replies = [line.strip("-• ").strip() for line in full_text.split("\n") if line.strip()]
        return replies[:2]
    except Exception as e:
        print("❌ OpenAI Error:", str(e))
        return [f"❌ Error: {str(e)}", ""]

@app.route('/api', methods=['POST'])
def receive_text():
    data = request.get_json()
    user_text = data.get("text", "")

    try:
        replies = get_chatgpt_reply(user_text)

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
