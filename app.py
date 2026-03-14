import os
from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai
import random

app = Flask(__name__)

# إعداد الجيمناي
API_KEY = "AIzaSyAUpdlOcI56F-S4rqzwXxOdlYNXz-Zv1pA"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

HTML = '''
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>راحة - عبد الرحمن حنكش</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * { box-sizing: border-box; }
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: #000; font-family: 'Segoe UI', Tahoma, sans-serif; }
        #intro-video { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; object-fit: cover; z-index: 100; background: #000; }
        #main-bg { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: url('https://i.postimg.cc/j5SypKL3/3ee9b6a30faf3d72302f46ae990495f1.jpg') no-repeat center center; background-size: cover; z-index: 1; display: none; }
        .overlay-dark { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.75); z-index: 2; display: none; }
        .content-wrapper { position: relative; z-index: 10; height: 100vh; display: flex; justify-content: center; align-items: center; display: none; }
        .card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(20px); padding: 25px; border-radius: 35px; width: 95%; max-width: 450px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.1); color: white; box-shadow: 0 25px 50px rgba(0,0,0,0.5); }
        .btn { display: block; width: 100%; padding: 14px; margin: 10px 0; border-radius: 50px; border: none; font-weight: bold; cursor: pointer; text-decoration: none; font-size: 16px; transition: 0.3s; text-align: center; }
        .btn-start { background: #fff; color: #000; box-shadow: 0 0 20px rgba(255,255,255,0.4); }
        .btn-wa { background: #25D366; color: white; }
        .btn-ig { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); color: white; }
        input { width: 100%; padding: 15px; margin: 10px 0; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); text-align: right; background: rgba(255,255,255,0.1); color: #fff; outline: none; }
        #chat-area { display: none; flex-direction: column; height: 480px; }
        #chat-box { flex: 1; overflow-y: auto; padding: 10px; display: flex; flex-direction: column; gap: 12px; margin-bottom: 10px; scroll-behavior: smooth; }
        .msg { padding: 12px 18px; border-radius: 22px; font-size: 14.5px; line-height: 1.5; max-width: 80%; animation: fadeIn 0.3s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .user { background: #3a7bd5; color: #fff; align-self: flex-end; border-bottom-right-radius: 4px; }
        .ai { background: rgba(255, 255, 255, 0.15); color: #fff; align-self: flex-start; border-bottom-left-radius: 4px; border: 1px solid rgba(255,255,255,0.1); }
        .chat-input-container { display: flex; gap: 8px; align-items: center; background: rgba(255,255,255,0.05); padding: 5px; border-radius: 25px; border: 1px solid rgba(255,255,255,0.1); }
        .chat-input-container input { border: none; background: transparent; margin: 0; padding: 10px; flex: 1; }
        .send-btn { background: #fff; color: #000; border: none; width: 45px; height: 45px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; }
        .dev-credit { margin-top: 20px; font-size: 13px; color: rgba(255,255,255,0.7); }
        .glow-name { color: #f1c40f; font-weight: bold; text-shadow: 0 0 10px #f1c40f; }
    </style>
</head>
<body>
    <audio id="sound-click" src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"></audio>
    <audio id="sound-send" src="https://assets.mixkit.co/active_storage/sfx/2358/2358-preview.mp3"></audio>
    <audio id="sound-receive" src="https://assets.mixkit.co/active_storage/sfx/2354/2354-preview.mp3"></audio>
    <video id="intro-video" autoplay muted playsinline><source src="https://f.top4top.io/m_3725bsi0i0.mp4" type="video/mp4"></video>
    <div id="main-bg"></div>
    <div id="main-overlay" class="overlay-dark"></div>
    <div class="content-wrapper" id="main-ui">
        <div class="card">
            <h1 id="title" style="color:#fff; text-shadow: 0 0 15px rgba(255,255,255,0.8); margin-bottom: 20px;">🌿 راحة</h1>
            <div id="menu">
                <button class="btn btn-start" onclick="playClick(); showInput()">ابدأ الجلسة العلاجية</button>
                <a href="https://wa.me/qr/GH6YWQHK3E2JI1" target="_blank" class="btn btn-wa" onclick="playClick()"><i class="fab fa-whatsapp"></i> واتساب</a>
                <a href="https://www.instagram.com/w.gza?utm_source=qr&igsh=MWhibXl2MGh5ZGY3bw==" target="_blank" class="btn btn-ig" onclick="playClick()"><i class="fab fa-instagram"></i> إنستجرام</a>
            </div>
            <div id="info-form" style="display:none;">
                <p id="prompt-text" style="font-size: 18px; margin-bottom: 15px;">ما اسمك؟</p>
                <input type="text" id="data-field" placeholder="اكتب هنا...">
                <button class="btn btn-start" onclick="playClick(); nextStep()">متابعة</button>
            </div>
            <div id="chat-area">
                <div id="chat-box"></div>
                <div class="chat-input-container">
                    <input type="text" id="msg-input" placeholder="اكتب ما تشعر به.." onkeypress="if(event.key==='Enter') sendMessage()">
                    <button class="send-btn" onclick="sendMessage()"><i class="fas fa-paper-plane"></i></button>
                </div>
            </div>
            <div class="dev-credit">برمجة وتطوير: <span class="glow-name">عبد الرحمن حنكش</span></div>
        </div>
    </div>
    <script>
        const v = document.getElementById('intro-video');
        v.onended = () => { v.style.display = 'none'; document.getElementById('main-bg').style.display = 'block'; document.getElementById('main-overlay').style.display = 'block'; document.getElementById('main-ui').style.display = 'flex'; };
        function playClick() { document.getElementById('sound-click').play(); }
        function playSend() { document.getElementById('sound-send').play(); }
        function playReceive() { document.getElementById('sound-receive').play(); }
        let step = 0; let user = { name: '', age: '' };
        function showInput() { document.getElementById('menu').style.display = 'none'; document.getElementById('info-form').style.display = 'block'; }
        function nextStep() {
            const field = document.getElementById('data-field'); if(!field.value) return;
            if(step === 0) { user.name = field.value; document.getElementById('prompt-text').innerText = `أهلاً ${user.name}، كم عمرك؟`; field.value = ''; field.type = 'number'; step = 1; }
            else { user.age = field.value; document.getElementById('info-form').style.display = 'none'; document.getElementById('chat-area').style.display = 'flex'; playReceive(); addMsg('ai', `أهلاً بك يا ${user.name} في منصة راحة. كيف حال قلبك اليوم؟`); }
        }
        async function sendMessage() {
            const input = document.getElementById('msg-input'); const text = input.value; if(!text) return;
            playSend(); addMsg('user', text); input.value = '';
            const res = await fetch('/get_ai_response', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({prompt: text, name: user.name, age: user.age}) });
            const data = await res.json(); setTimeout(() => { playReceive(); addMsg('ai', data.answer); }, 400);
        }
        function addMsg(cls, txt) { const b = document.getElementById('chat-box'); b.innerHTML += `<div class="msg ${cls}">${txt}</div>`; b.scrollTop = b.scrollHeight; }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/get_ai_response', methods=['POST'])
def get_ai_response():
    d = request.json
    instruction = f"أنت طبيب نفسي مصري اسمك راحة، بتعالج المريض {d['name']} (سن {d['age']}). رد بذكاء وحنية وبالعامية المصرية."
    try:
        response = model.generate_content(instruction + "\\n" + d['prompt'])
        return jsonify({"answer": response.text})
    except:
        return jsonify({"answer": "أنا معاك، فضفض أكتر.."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
