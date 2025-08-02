from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# DB setup
def save_message(username, message):
    conn = sqlite3.connect('chat.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, message))
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return "Messaging server running."

@socketio.on("message")
def handle_message(data):
    print(f"Received: {data}")
    username = data.get("username", "Anonymous")
    message = data.get("message", "")
    save_message(username, message)
    send(data, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
