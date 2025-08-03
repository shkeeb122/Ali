from flask import Flask, request, render_template
import requests, json, os

app = Flask(__name__)

# 🔹 Backend Chatbot Endpoint (Render ya Railway)
CHAT_URL = "https://umar-y55h.onrender.com/chat"
HISTORY_FILE = "chat_history.json"

# 🔹 Chat history load
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# 🔹 Chat history save
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

# 🔹 Get Chatbot reply
def get_chat_response(prompt):
    try:
        res = requests.post(CHAT_URL, json={"message": prompt})
        return res.json().get("reply", "No reply received.")
    except:
        return "❌ Chatbot error!"

@app.route("/", methods=["GET", "POST"])
def index():
    history = load_history()
    reply = ""

    if request.method == "POST":
        prompt = request.form.get("prompt")
        reply = get_chat_response(prompt)
        history.append({"user": prompt, "bot": reply})
        save_history(history)

    return render_template("index.html", reply=reply, history=history)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
