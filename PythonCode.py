from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# مفتاح OpenAI API (يفضل تخزينه في متغير بيئة لاحقًا)
openai.api_key = "YOUR_OPENAI_API_KEY"  # ← استبدليه بمفتاحك الحقيقي

@app.route('/api', methods=['POST'])
def receive_text():
    data = request.get_json()
    user_text = data.get("text", "")

    print(f"📥 Received text: {user_text}")

    # البرومت الذكي
    prompt = f"""
أنا أطور جهاز يساعد الصم والبكم على التواصل. المستخدم قال: "{user_text}"
اقترح ردين يعبرون عن رغبة المستخدم فقط، باللهجة الخليجية أو العربية البسيطة.
لا تتقمص دور الطرف الآخر.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )

        reply_text = response["choices"][0]["message"]["content"]
        replies = [line.strip("-• ").strip() for line in reply_text.split("\n") if line.strip()]

        return jsonify({
            "reply_1": replies[0] if len(replies) > 0 else "",
            "reply_2": replies[1] if len(replies) > 1 else ""
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

# لا نستخدم app.run() لأن Render يشغّل السيرفر باستخدام gunicorn
