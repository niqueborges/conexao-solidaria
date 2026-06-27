// Function to get the CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to generate a new session_id when the page loads
function generateSessionId() {
    const sessionId = crypto.randomUUID();
    sessionIdInput.value = sessionId;
}

// Get the CSRF token
const csrftoken = getCookie('csrftoken');

// DOM elements
const form = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const sessionIdInput = document.getElementById("session_id");
const chatBox = document.getElementById("chat-box");
const clearChatButton = document.getElementById("clear-chat");
const imageInput = document.getElementById("image");
const imagePreview = document.getElementById("image-preview");
const typingIndicator = document.getElementById("typing-indicator");

// Handle image preview
imageInput.addEventListener("change", () => {
    if (imageInput.files.length > 0) {
        imagePreview.style.display = "block";
        imagePreview.textContent = `Arquivo selecionado: ${imageInput.files[0].name}`;
    } else {
        imagePreview.style.display = "none";
    }
});

function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

function getFormattedTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Function to display SoliBot's response
function displayBotResponse(data) {
    if (data.error) {
        const errorHtml = `
            <div class="msg-container bot">
                <div class="msg-bubble" style="background-color: #ef4444; color: white;">
                    Erro: ${data.error}
                </div>
                <span class="msg-time">${getFormattedTime()}</span>
            </div>`;
        typingIndicator.insertAdjacentHTML('beforebegin', errorHtml);
    } else {
        data.lex.forEach((msg) => {
            const html = `
                <div class="msg-container bot">
                    <div class="msg-bubble">
                        ${msg['content'].replace(/#/g, '<br>')}
                    </div>
                    <span class="msg-time">${getFormattedTime()}</span>
                </div>`;
            typingIndicator.insertAdjacentHTML('beforebegin', html);
        });
    }
    scrollToBottom();
}

// Form submission to send a message or image to the backend
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const message = messageInput.value.trim();
    const sessionId = sessionIdInput.value;
    const imageFile = imageInput.files[0];

    if (!message && !imageFile) return;

    if (message) {
        const userHtml = `
            <div class="msg-container user">
                <div class="msg-bubble">${message}</div>
                <span class="msg-time">${getFormattedTime()}</span>
            </div>`;
        typingIndicator.insertAdjacentHTML('beforebegin', userHtml);
    } else if (imageFile) {
        const userHtml = `
            <div class="msg-container user">
                <div class="msg-bubble">📷 <em>Imagem enviada</em></div>
                <span class="msg-time">${getFormattedTime()}</span>
            </div>`;
        typingIndicator.insertAdjacentHTML('beforebegin', userHtml);
    }

    messageInput.value = '';
    imageInput.value = '';
    imagePreview.style.display = "none";
    
    // Show typing indicator
    typingIndicator.style.display = "flex";
    scrollToBottom();

    const formData = new FormData();
    formData.append("session_id", sessionId);

    if (message) formData.append("message", message);
    if (imageFile) formData.append("image", imageFile);

    try {
        const response = await fetch("/chatbot/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: formData,
        });

        const data = await response.json();
        
        // Hide typing indicator
        typingIndicator.style.display = "none";
        
        displayBotResponse(data);
    } catch (error) {
        console.error("Request error:", error);
        typingIndicator.style.display = "none";
    }
});

// Clear the chat
clearChatButton.addEventListener("click", () => {
    // Keep only the welcome message and typing indicator
    const welcomeHtml = `
        <div class="msg-container bot">
            <div class="msg-bubble">
                Olá! Eu sou o SoliBot, o assistente virtual do Conexão Solidária.<br><br>
                Como posso ajudar você a transformar uma vida hoje?
            </div>
            <span class="msg-time">${getFormattedTime()}</span>
        </div>`;
    
    chatBox.innerHTML = welcomeHtml;
    chatBox.appendChild(typingIndicator);
});

// Generate a new session_id when the page loads
document.addEventListener("DOMContentLoaded", generateSessionId);
