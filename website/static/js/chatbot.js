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
const recordAudioButton = document.getElementById("record-audio");

let mediaRecorder;
let audioChunks = [];
let audioBlob = null;

// Function to send the audio to the backend
async function sendAudio(audioBlob, sessionId) {
    const formData = new FormData();
    formData.append("session_id", sessionId);
    formData.append("audio", audioBlob, "recording.webm");

    try {
        const response = await fetch("/chatbot/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: formData,
        });

        if (!response.ok) {
            console.error("Server response error:", response.status, response.statusText);
            chatBox.innerHTML += `
                <div class="d-flex justify-content-start mb-2">
                    <div class="bg-danger text-white p-2 rounded" style="max-width: 70%;">
                        <strong>Error:</strong> Server response processing error.
                    </div>
                </div>`;
            return;
        }

        const data = await response.json();
        displayBotResponse(data);

    } catch (error) {
        console.error("Audio request error:", error);
        chatBox.innerHTML += `
            <div class="d-flex justify-content-start mb-2">
                <div class="bg-danger text-white p-2 rounded" style="max-width: 70%;">
                    <strong>Error:</strong> Unable to send audio. Please try again.
                </div>
            </div>`;
    }
}

// Function to display SoliBot's response
function displayBotResponse(data) {
    if (data.error) {
        chatBox.innerHTML += `
            <div class="d-flex justify-content-start mb-2">
                <div class="bg-danger text-white p-2 rounded" style="max-width: 70%;">
                    <strong>Error:</strong> ${data.error}
                </div>
            </div>`;
    } else {
        data.lex.forEach((msg) => {
            chatBox.innerHTML += `
                <div class="d-flex justify-content-start mb-2">
                    <div class="bg-secondary-subtle text-dark p-2 rounded" style="max-width: 70%;">
                        <strong>SoliBot:</strong> ${msg['content']}
                    </div>
                </div>`;
        });
    }
    chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to the end of the chat
}

// Form submission to send a message to the backend
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const message = messageInput.value.trim();
    const sessionId = sessionIdInput.value;

    if (message) {
        // Display the user's message in the chat
        chatBox.innerHTML += `
            <div class="d-flex justify-content-end mb-2">
                <div class="bg-success-subtle text-dark p-2 rounded" style="max-width: 70%;">
                    <strong>You:</strong> ${message}
                </div>
            </div>`;

        messageInput.value = '';  // Clear the input field

        // Prepare the data for sending
        const formData = new FormData();
        formData.append("message", message);
        formData.append("session_id", sessionId);

        if (audioBlob) {
            formData.append("audio", audioBlob, "recording.webm");
            audioBlob = null;
        }

        try {
            const response = await fetch("/chatbot/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                },
                body: formData,
            });

            const data = await response.json();
            displayBotResponse(data);
        } catch (error) {
            console.error("Request error:", error);
        }
    }
});

// Clear the chat when clicking the "Clear Chat" button
clearChatButton.addEventListener("click", () => {
    chatBox.innerHTML = '';
});

// Handles the audio recording button
recordAudioButton.addEventListener("click", async () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        recordAudioButton.textContent = "Record Audio";
        return;
    }

    if (!mediaRecorder) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.addEventListener("dataavailable", (event) => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                audioBlob = new Blob(audioChunks, { type: "audio/webm" });
                audioChunks = [];
                sendAudio(audioBlob, sessionIdInput.value);  // Sends the audio after stopping recording
            });
        } catch (error) {
            alert("Unable to access the microphone.");
            console.error("Microphone access error:", error);
            return;
        }
    }

    mediaRecorder.start();
    recordAudioButton.textContent = "Stop Recording";
});

// Generate a new session_id when the page loads
document.addEventListener("DOMContentLoaded", generateSessionId);
