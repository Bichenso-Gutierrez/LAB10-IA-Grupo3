const chatBox = document.getElementById("chat-box");
const input = document.getElementById("pregunta");

function agregarMensaje(texto, tipo) {
    const bubble = document.createElement("div");
    bubble.classList.add("bubble");

    if (tipo === "user") {
        bubble.classList.add("user-msg");
    } else {
        bubble.classList.add("bot-msg");
    }

    bubble.textContent = texto;
    chatBox.appendChild(bubble);

    // Scroll automático
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function enviarMensaje() {
    const msg = input.value.trim();
    if (msg === "") return;

    // Mostrar mensaje del usuario
    agregarMensaje(msg, "user");
    input.value = "";

    // Llamar al backend Flask / Python
    const respuesta = await fetch("/consulta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pregunta: msg })
    });

    const data = await respuesta.json();

    // Mostrar respuesta del bot
    agregarMensaje(data.respuesta, "bot");
}

// Enviar con Enter
input.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        enviarMensaje();
    }
});
