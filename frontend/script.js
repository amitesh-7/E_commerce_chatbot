const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const chatMessages = document.getElementById("chat-messages");
const chatWindow = document.getElementById("chat-window");

const sessionId = `session_${Math.random().toString(36).substr(2, 9)}`;

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userMessage = messageInput.value.trim();
  if (!userMessage) return;

  addMessage(userMessage, "user-message");
  messageInput.value = "";

  try {
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: userMessage, session_id: sessionId }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    addMessage(data.response, "bot-message");
  } catch (error) {
    console.error("Fetch Error:", error);
    addMessage("Sorry, something went wrong. Please try again.", "bot-message");
  }
});

function addMessage(text, className) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("message", className);
  messageElement.textContent = text;
  chatMessages.appendChild(messageElement);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
