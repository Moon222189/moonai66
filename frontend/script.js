async function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value;
    if (!message) return;
    input.value = "";

    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<p><b>You:</b> ${message}</p>`;

    const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    });

    const data = await response.json();
    chatbox.innerHTML += `<p><b>MoonAI:</b> ${data.response}</p>`;
    chatbox.scrollTop = chatbox.scrollHeight;
}
