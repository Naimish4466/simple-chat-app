from flask import Flask, render_template
from flask_socketio import SocketIO, send
from database import init_db, save_message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    username = data.get("username")
    message = data.get("message")
    save_message(username, message)
    send({'username': username, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
print(f"Received from {username}: {message}")
