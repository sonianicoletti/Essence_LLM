// Function to handle sending the message
async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const query = inputField.value.trim();  // Trim extra spaces
    if (!query) return;  // Do nothing if the input is empty

    // Display user message in chatbox on the right
    const chatbox = document.getElementById('chatbox');
    chatbox.innerHTML += `<div class="message user-message">${query}</div>`;
    inputField.value = '';  // Clear the input field

    // Display the loading indicator for bot response
    const loadingIndicator = document.createElement('div');
    loadingIndicator.classList.add('message', 'bot-message');
    loadingIndicator.innerHTML = `
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>`;
    chatbox.appendChild(loadingIndicator);
    chatbox.scrollTop = chatbox.scrollHeight;  // Scroll to the bottom

    // Send query to the backend
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
    });

    const data = await response.json();

    // Remove the loading indicator
    chatbox.removeChild(loadingIndicator);

    // Display bot message in chatbox on the left
    chatbox.innerHTML += `<div class="message bot-message">${data.response}</div>`;
    chatbox.scrollTop = chatbox.scrollHeight;  // Scroll to the bottom
}

// Detect 'Enter' key press and send message
const inputField = document.getElementById('user-input');
inputField.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});
