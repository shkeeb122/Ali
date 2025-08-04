from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)

HISTORY_FILE = "chat_history.json"

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

    # 🔹 Real bot ka reply yahan connect kar sakte ho
    bot_reply = f"🤖 Bot: '{user_message}' ka jawab yeh hai!"

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
