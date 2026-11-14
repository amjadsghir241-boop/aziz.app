from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# ضع مفتاح الـ API الخاص بك هنا كاملاً ودون أسطر جديدة
GEMINI_API_KEY = "AQ.Ab8RN6L909wUsCy1UthfQ0jWjzmW_8j4xMReoEXIfmlm2izuAA"

# واجهة المستخدم (HTML) المدمجة
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>المساعد الفقهي الميسر</title>
    <style>
        body { font-family: Tahoma, sans-serif; background: #f4f4f9; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #333; }
        .chat-box { height: 350px; border: 1px solid #ddd; border-radius: 5px; padding: 10px; overflow-y: scroll; margin-bottom: 15px; background: #fafafa; }
        .message { margin-bottom: 10px; padding: 8px 12px; border-radius: 5px; line-height: 1.5; }
        .user { background: #e3f2fd; text-align: right; }
        .bot { background: #f1f8e9; text-align: right; }
        .input-group { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; outline: none; }
        button { padding: 10px 20px; background: #1976d2; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #115293; }
    </style>
</head>
<body>
    <div class="container">
        <h2>المساعد الفقهي الميسر</h2>
        <div class="chat-box" id="chatBox">
            <div class="message bot"><b>المساعد:</b> أهلاً بك، كيف يمكنني مساعدتك في المسائل الفقهية اليوم؟</div>
        </div>
        <div class="input-group">
            <input type="text" id="userInput" placeholder="اكتب سؤالك هنا..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">إرسال</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const inputField = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const message = inputField.value.trim();
            if (!message) return;

            chatBox.innerHTML += `<div class="message user"><b>أنت:</b> ${message}</div>`;
            inputField.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                chatBox.innerHTML += `<div class="message bot"><b>المساعد:</b> ${data.response}</div>`;
            } catch (error) {
                chatBox.innerHTML += `<div class="message bot" style="color:red;"><b>المساعد:</b> حدث خطأ في الاتصال.</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
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
        # رابط النموذج القياسي بدون ?key=
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        prompt_text = f"أنت مساعد فقهي ميسر. أجب باختصار ووضوح مستنداً إلى الأدلة إن أمكن. السؤال هو: {user_message}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }]
        }
        
        # تمرير المفتاح عبر الترويسات (Headers) كـ Bearer Token
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GEMINI_API_KEY}'
        }
        
        res = requests.post(url, json=payload, headers=headers)
        res_json = res.json()
        
        if res.status_code == 200:
            bot_reply = res_json['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'response': bot_reply})
        else:
            error_msg = res_json.get('error', {}).get('message', 'خطأ غير معروف')
            return jsonify({'response': f'خطأ من المزود: {error_msg}'})
            
    except Exception as e:
        return jsonify({'response': f'حدث استثناء في الخادم: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
