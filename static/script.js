async function sendMessage() {
    const input = document.getElementById("user-input");
    const msg = input.value.trim();
    if (!msg) return;
    addMessage("user", msg);
    input.value = "";

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg, session: currentSession })
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

async function createSession() {
    const name = prompt("Enter new session name:");
    if (!name) return;
    const res = await fetch("/new_session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    });
    const data = await res.json();
    if (data.status === "created") location.reload();
}

async function loadSession(name) {
    currentSession = name;
    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: "", session: currentSession })
    });
    const data = await res.json();
    document.getElementById("chat-box").innerHTML = "";
    data.history.forEach(m => {
        addMessage("user", m.user);
        addMessage("bot", m.bot);
    });
}

async function clearSession() {
    await fetch("/clear_session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session: currentSession })
    });
    document.getElementById("chat-box").innerHTML = "";
}

function downloadSession() {
    window.location.href = `/download/${currentSession}`;
}
