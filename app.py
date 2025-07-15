from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Chatbot backend (your Render-hosted chatbot endpoint)
CHAT_URL = "https://umar-y55h.onrender.com/chat"

# HuggingFace image model endpoint
IMAGE_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HF_TOKEN = "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"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# 🔷 Generate image from prompt
def generate_image(prompt):
    response = requests.post(IMAGE_URL, headers=HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        with open("static/generated.png", "wb") as f:
            f.write(response.content)
    else:
        print("Image generation failed:", response.text)

# 🔷 Get chatbot reply
def get_chat_response(prompt):
    try:
        res = requests.post(CHAT_URL, json={"message": prompt})
        return res.json().get("reply", "No reply received.")
    except:
        return "❌ Chatbot error!"

# 🔷 Main route
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

# 🔷 Render-compatible app run command
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
