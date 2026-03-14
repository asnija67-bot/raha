import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# المفتاح بتاعك
API_KEY = "AIzaSyAUpdlOcI56F-S4rqzwXxOdlYNXz-Zv1pA"

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>منصة راحة</title>
        <style>
            body { font-family: sans-serif; background: #fdfbff; margin: 0; display: flex; flex-direction: column; height: 100vh; }
            .header { background: #6750a4; color: white; padding: 15px; text-align: center; font-weight: bold; }
            .chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 10px; }
            .msg { max-width: 80%; padding: 10px 15px; border-radius: 15px; }
            .user { align-self: flex-start; background: #eaddff; }
            .ai { align-self: flex-end; background: #ffffff; border: 1px solid #ccc; }
            .input-area { padding: 15px; display: flex; gap: 10px; border-top: 1px solid #ddd; padding-bottom: 30px; }
            input { flex: 1; padding: 12px; border-radius: 25px; border: 1px solid #79747e; }
            button { background: #6750a4; color: white; border: none; padding: 10px 20px; border-radius: 25px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="header">منصة راحة ✨</div>
        <div class="chat-container" id="chat">
            <div class="msg ai">أهلاً بيك يا صديقي.. حابب تحكي لي عن إيه؟</div>
        </div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="فضفض هنا...">
            <button onclick="send()">إرسال</button>
        </div>
        <script>
            async function send() {
                const input = document.getElementById('user-input');
                const chat = document.getElementById('chat');
                const text = input.value.trim();
                if(!text) return;
                chat.innerHTML += `<div class="msg user">${text}</div>`;
                input.value = '';
                const res = await fetch('/get_ai_response', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                chat.innerHTML += `<div class="msg ai">${data.answer}</div>`;
                chat.scrollTop = chat.scrollHeight;
            }
        </script>
    </body>
    </html>
    """

@app.route('/get_ai_response', methods=['POST'])
def get_ai_response():
    user_msg = request.json.get('message', '')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"أنت أخصائي نفسي مصري حكيم، رد بالعامية المصرية: {user_msg}"}]}]
    }
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        # هنا التعديل عشان نضمن سحب النص صح
        answer = data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"يا صاحبي حصل مشكلة: {str(e)[:50]}"})

app = app
if __name__ == "__main__":
    app.run()
    
