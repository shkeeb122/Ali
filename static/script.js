async function sendMessage() {
    const input = document.getElementById("user-input");
    const msg = input.value.trim();
    if (!msg) return;

    addMessage("user", msg);
    input.value = "";

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    addMessage("bot", data.reply);
}

function addMessage(sender, text) {
    const box = document.getElementById("chat-box");
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    div.textContent = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}

function loadMessage(user, bot) {
    const box = document.getElementById("chat-box");
    box.innerHTML = `
      <div class="message user">${user}</div>
      <div class="message bot">${bot}</div>
    `;
}

async function clearHistory() {
    await fetch("/clear", { method: "POST" });
    document.getElementById("history-list").innerHTML = "";
    document.getElementById("chat-box").innerHTML = "";
}
