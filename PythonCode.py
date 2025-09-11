from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_audio():
    with open("received.wav", "wb") as f:
        f.write(request.data)
    return "تم الاستلام"

app.run(host='0.0.0.0', port=5000)