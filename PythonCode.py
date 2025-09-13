from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/api', methods=['POST'])
def receive_text():
    data = request.get_json()
    user_text = data.get("text", "")

    prompt = f"""
أنا أطور جهاز يساعد الصم والبكم على التواصل. المستخدم قال: "{user_text}"
اقترح ردين يعبرون عن رغبة المستخدم فقط، باللهجة الخليجية أو العربية البسيطة.
لا تتقمص دور الطرف الآخر.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        reply_text = response.choices[0].message.content
        replies = [line.strip("-• ").strip() for line in reply_text.split("\n") if line.strip()]

        return jsonify({
            "reply_1": replies[0] if len(replies) > 0 else "",
            "reply_2": replies[1] if len(replies) > 1 else ""
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

