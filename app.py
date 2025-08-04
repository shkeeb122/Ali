from flask import Flask, render_template, request, jsonify
import json, os, requests

app = Flask(__name__)

HISTORY_FILE = "chat_history.json"
CHATBOT_URL = "https://umar-y55h.onrender.com/chat"  # Tumhara backend

# Ensure history file exists
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def load_history():
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

@app.route("/")
def index():
    history = load_history()
    return render_template("index.html", history=history)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    history = load_history()

    # ✅ Real Chatbot se reply lo
    try:
        res = requests.post(CHATBOT_URL, json={"message": user_message}, timeout=10)
        if res.status_code == 200:
            bot_reply = res.json().get("reply", "❌ Bot se reply nahi mila")
        else:
            bot_reply = "❌ Bot down ya error"
    except:
        bot_reply = "❌ Backend se connect nahi ho paaya"

    # History update
    history.append({"user": user_message, "bot": bot_reply})
    save_history(history)

    return jsonify({"reply": bot_reply, "history": history})

@app.route("/clear", methods=["POST"])
def clear_history():
    save_history([])
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
