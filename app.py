from flask import Flask, render_template, request, jsonify, send_file
import json, os, requests
from datetime import datetime

app = Flask(__name__)

HISTORY_FILE = "chat_history.json"
CHATBOT_URL = "https://umar-y55h.onrender.com/chat"  # Tumhara backend

# Ensure file exists
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump({"sessions": {}}, f)

def load_data():
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f)

@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", sessions=data["sessions"])

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    session_id = request.json.get("session", "default")
    data = load_data()
    if session_id not in data["sessions"]:
        data["sessions"][session_id] = []

    # Bot reply
    try:
        res = requests.post(CHATBOT_URL, json={"message": user_message}, timeout=10)
        bot_reply = res.json().get("reply", "❌ Bot reply nahi mila") if res.status_code == 200 else "❌ Bot error"
    except:
        bot_reply = "❌ Backend connect nahi ho paaya"

    # Save
    msg = {"user": user_message, "bot": bot_reply, "time": datetime.now().strftime("%H:%M:%S")}
    data["sessions"][session_id].append(msg)
    save_data(data)

    return jsonify({"reply": bot_reply, "history": data["sessions"][session_id]})

@app.route("/new_session", methods=["POST"])
def new_session():
    name = request.json.get("name", f"Session-{datetime.now().strftime('%H%M%S')}")
    data = load_data()
    data["sessions"][name] = []
    save_data(data)
    return jsonify({"status": "created", "session": name})

@app.route("/clear_session", methods=["POST"])
def clear_session():
    session_id = request.json.get("session", "default")
    data = load_data()
    data["sessions"][session_id] = []
    save_data(data)
    return jsonify({"status": "cleared"})

@app.route("/download/<session_id>")
def download_session(session_id):
    data = load_data()
    chat = data["sessions"].get(session_id, [])
    file_name = f"{session_id}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        for m in chat:
            f.write(f"👤 {m['user']}\n🤖 {m['bot']}\n\n")
    return send_file(file_name, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
