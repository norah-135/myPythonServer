from flask import Flask, request

app = Flask(__name__)

# مسار استقبال ملفات صوتية (إذا احتجتيه لاحقًا)
@app.route('/upload', methods=['POST'])
def upload_audio():
    with open("received.wav", "wb") as f:
        f.write(request.data)
    return "🎧 تم استلام الملف الصوتي"

# مسار استقبال نصوص من الأردوينو
@app.route('/api', methods=['POST'])
def receive_text():
    data = request.get_json()
    print("📥 Received text:", data['text'])
    return "✅ Received text", 200

# تشغيل السيرفر
# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000) 

