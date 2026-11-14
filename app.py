import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# مفتاح الـ API الخاص بك
GEMINI_API_KEY = "AQ.Ab8RN6KOUag3XtrxNaTlWDYYMSyvNREopu4ZgMkO7iYX7M32Ow"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>المساعد الفقهي الميسر</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9fb; color: #333; }
        .chat-container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        #chat-box { height: 300px; border: 1px solid #ddd; border-radius: 4px; padding: 10px; overflow-y: auto; margin-bottom: 15px; background: #fff; }
        .message { margin-bottom: 10px; padding: 8px; border-radius: 5px; }
        .user-msg { background: #e3f2fd; text-align: right; }
        .bot-msg { background: #f1f8e9; text-align: right; }
        input[type="text"] { width: 75%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        button { width: 20%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h2>المساعد الفقهي الميسر</h2>
        <div id="chat-box"></div>
        <div style="display: flex; justify-content: space-between;">
            <input type="text" id="user-input" placeholder="اكتب سؤالك هنا..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">إرسال</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const inputField = document.getElementById('user-input');
            const chatBox = document.getElementById('chat-box');
            const message = inputField.value.trim();
            if (!message) return;

            chatBox.innerHTML += `<div class="message user-msg"><b>أنت:</b> ${message}</div>`;
            inputField.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                chatBox.innerHTML += `<div class="message bot-msg"><b>المساعد:</b> ${data.response}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (error) {
                chatBox.innerHTML += `<div class="message bot-msg" style="color:red;">حدث خطأ في الاتصال.</div>`;
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '') if data else ''
    if not user_message:
        return jsonify({'response': 'المرجو إدخال سؤال.'})
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        prompt_text = f"أنت مساعد فقهي ميسر. أجب باختصار ووضوح مستنداً إلى الأدلة إن أمكن. السؤال هو: {user_message}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }]
        }
        
        res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        res_data = res.json()
        
        if 'candidates' in res_data:
            reply = res_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'response': reply})
        else:
            return jsonify({'response': f"خطأ من المزود: {res_data}"})
            
    except Exception as e:
        return jsonify({'response': f'حدث خطأ في الاتصال: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
