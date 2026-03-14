import os
from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# المفتاح الخاص بك
API_KEY = "AIzaSyAUpdlOcI56F-S4rqzwXxOdlYNXz-Zv1pA"
genai.configure(api_key=API_KEY)

# استخدام النسخة الأكثر استقراراً على الإطلاق
model = genai.GenerativeModel('gemini-1.0-pro')

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة راحة</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #fdfbff; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        .header { background: #6750a4; color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 20px; }
        .chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .msg { max-width: 85%; padding: 12px 18px; border-radius: 18px; font-size: 16px; line-height: 1.6; }
        .user { align-self: flex-start; background: #eaddff; color: #21005d; border-bottom-left-radius: 4px; }
        .ai { align-self: flex-end; background: #ffffff; color: #1c1b1f; border: 1px solid #cac4d0; border-bottom-right-radius: 4px; }
        .input-area { background: white; padding: 15px; display: flex; gap: 10px; border-top: 1px solid #ddd; padding-bottom: 30px; }
        input { flex: 1; padding: 12px; border: 1px solid #79747e; border-radius: 25px; outline: none; }
        button { background: #6750a4; color: white; border: none; padding: 10px 22px; border-radius: 25px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">منصة راحة ✨</div>
    <div class="chat-container" id="chat">
        <div class="msg ai">أهلاً بيك يا صديقي في "راحة".. أنا هنا عشان أسمعك. حابب تحكي لي عن إيه؟</div>
    </div>
    <div class="input-area">
        <input type="text" id="user-input" placeholder="فضفض هنا..." onkeypress="if(event.key==='Enter') send()">
        <button id="send-btn" onclick="send()">إرسال</button>
    </div>
    <script>
        async function send() {
            const input = document.getElementById('user-input');
            const chat = document.getElementById('chat');
            const btn = document.getElementById('send-btn');
            const text = input.value.trim();
            if(!text) return;
            chat.innerHTML += `<div class="msg user">${text}</div>`;
            input.value = '';
            btn.disabled = true;
            try {
                const res = await fetch('/get_ai_response', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                chat.innerHTML += `<div class="msg ai">${data.answer}</div>`;
            } catch (e) {
                chat.innerHTML += `<div class="msg ai">حصلت مشكلة صغيرة.. حاول تاني.</div>`;
            }
            btn.disabled = false;
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/get_ai_response', methods=['POST'])
def get_ai_response():
    data = request.json
    user_msg = data.get('message', '')
    try:
        # صياغة الطلب بشكل بسيط جداً
        response = model.generate_content(f"أنت أخصائي نفسي مصري، رد بالعامية المصرية على: {user_msg}")
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"answer": f"يا بطل، حصل خطأ: {str(e)[:50]}"})

app = app
if __name__ == "__main__":
    app.run()
