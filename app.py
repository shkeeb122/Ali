from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Chatbot backend (render link)
CHAT_URL = "https://umar-y55h.onrender.com/chat"

# HuggingFace image model
IMAGE_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HF_TOKEN = "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"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def generate_image(prompt):
    response = requests.post(IMAGE_URL, headers=HEADERS, json={"inputs": prompt})
    with open("static/generated.png", "wb") as f:
        f.write(response.content)

def get_chat_response(prompt):
    try:
        res = requests.post(CHAT_URL, json={"message": prompt})
        return res.json().get("reply", "No reply received.")
    except:
        return "❌ Chatbot error!"

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    image = None
    if request.method == "POST":
        prompt = request.form.get("prompt")
        action = request.form.get("action")
        if action == "chat":
            reply = get_chat_response(prompt)
        elif action == "image":
            generate_image(prompt)
            image = "static/generated.png"
    return render_template("index.html", reply=reply, image=image)

if __name__ == "__main__":
    app.run(debug=True)
