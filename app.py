import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# مفتاحك السليم
API_KEY = "AIzaSyC-FtNsao7WdY17dJWQbKivF_J6oDGQddg"

# رجعنا الموديل الحديث (1.5-flash) اللي جوجل بتدعمه دلوقتي
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

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
        button { background: #6750a4; color: white; border: none; padding: 10px 22px; border-radius: 25px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">منصة راحة ✨</div>
    <div class="chat-container" id="chat">
        <div class="msg ai">أهلاً بيك يا عبد الرحمن في "راحة".. أنا هنا عشان أسمعك، احكي لي.</div>
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
            chat.scrollTop = chat.scrollHeight;
            
            try {
                const res = await fetch('/get_ai_response', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                chat.innerHTML += `<div class="msg ai">${data.answer}</div>`;
            } catch (e) {
                chat.innerHTML += `<div class="msg ai">حصلت مشكلة تقنية.. حاول تاني.</div>`;
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
    user_msg = request.json.get('message', '')
    
    payload = {
        "contents": [{
            "parts": [{"text": f"أنت أخصائي نفسي مصري حكيم وحنون اسمك 'راحة'. رد بالعامية المصرية الدافئة على: {user_msg}"}]
        }]
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(URL, json=payload, headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            answer = data['candidates'][0]['content']['parts'][0]['text']
        else:
            answer = f"حصل مشكلة من جوجل: {data.get('error', {}).get('message', 'خطأ')}"
            
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": "السيرفر فيه عطل بسيط، جرب تبعت تاني."})

app = app
if __name__ == "__main__":
    app.run()
    
