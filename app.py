import os
from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

# إعداد التطبيق والذكاء الاصطناعي
app = Flask(__name__)

# وضعنا مفتاحك هنا وتأكدنا منه
genai.configure(api_key="AIzaSyAUpdlOcI56F-S4rqzwXxOdlYNXz-Zv1pA")
model = genai.GenerativeModel('gemini-1.5-flash')

# واجهة الموقع (HTML/CSS/JS) بتصميم هادئ ومريح
HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة راحة - صديقك النفسي</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #fdfbff; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        .header { background: #6750a4; color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .msg { max-width: 85%; padding: 12px 18px; border-radius: 18px; font-size: 16px; line-height: 1.6; }
        .user { align-self: flex-start; background: #eaddff; color: #21005d; border-bottom-left-radius: 4px; }
        .ai { align-self: flex-end; background: #ffffff; color: #1c1b1f; border: 1px solid #cac4d0; border-bottom-right-radius: 4px; }
        .input-area { background: white; padding: 15px; display: flex; gap: 10px; border-top: 1px solid #ddd; padding-bottom: 30px; }
        input { flex: 1; padding: 12px; border: 1px solid #79747e; border-radius: 25px; outline: none; font-size: 16px; }
        button { background: #6750a4; color: white; border: none; padding: 10px 22px; border-radius: 25px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">منصة راحة ✨</div>
    <div class="chat-container" id="chat">
        <div class="msg ai">أهلاً بيك يا صديقي في "راحة".. أنا هنا عشان أسمعك بكل هدوء. حابب تحكي لي عن إيه النهاردة؟</div>
    </div>
    <div class="input-area">
        <input type="text" id="user-input" placeholder="فضفض هنا..." onkeypress="if(event.key==='Enter') send()">
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
            chat.scrollTop = chat.scrollHeight;

            try {
                const res = await fetch('/get_ai_response', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: text})
                });
                const data = await res.json();
                chat.innerHTML += `<div class="msg ai">${data.answer}</div>`;
            } catch {
                chat.innerHTML += `<div class="msg ai">أنا سامعك، بس النت خانقني شوية.. كمل كلامك أنا معاك.</div>`;
            }
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
    
    # الشخصية: أخصائي نفسي مصري حكيم
    prompt = f"أنت أخصائي نفسي مصري حكيم وهادئ وحنون جداً، اسمك 'راحة'. مهمتك تسمع الناس وتطبطب عليهم بالعامية المصرية الدافئة وتساعدهم يتخطوا مشاكلهم. رد على الرسالة دي: {user_msg}"
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"answer": "معلش يا صاحبي، دماغي هنجت شوية.. قول لي تاني كدة كنت بتقول إيه؟"})

# التوافق مع Vercel
app = app
if __name__ == "__main__":
    app.run()
    
