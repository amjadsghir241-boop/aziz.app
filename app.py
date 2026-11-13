import os
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(_name_)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تطبيق الدردشة</title>
    <style>
        body { font-family: Arial, sans-serif; background: #ece5dd; margin: 0; padding: 20px; }
        #chat-box { background: white; max-width: 500px; margin: 0 auto; height: 400px; overflow-y: scroll; padding: 10px; border-radius: 5px; }
        .msg { margin-bottom: 10px; padding: 8px 12px; border-radius: 5px; background: #dcf8c6; }
        #form { max-width: 500px; margin: 10px auto; display: flex; gap: 10px; }
        input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { padding: 10px 20px; background: #075e54; color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
</head>
<body>
    <div id="chat-box"></div>
    <div id="form">
        <input id="input" autocomplete="off" placeholder="اكتب رسالة..." />
        <button onclick="send()">إرسال</button>
    </div>
    <script>
        const socket = io();
        socket.on('message', function(msg) {
            const item = document.createElement('div');
            item.className = 'msg';
            item.textContent = msg;
            document.getElementById('chat-box').appendChild(item);
            document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
        });
        function send() {
            const input = document.getElementById('input');
            if (input.value) {
                socket.emit('message', input.value);
                input.value = '';
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@socketio.on('message')
def handle_message(msg):
    emit('message', msg, broadcast=True)

if _name_ == '_main_':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
