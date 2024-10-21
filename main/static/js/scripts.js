async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const query = inputField.value;
    if (!query) return;

    // Display user message in chatbox
    const chatbox = document.getElementById('chatbox');
    chatbox.innerHTML += `<div>User: ${query}</div>`;
    inputField.value = '';  // Clear input field

    // Send query to the backend
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
    });

    const data = await response.json();
    // Display LLM response in chatbox
    chatbox.innerHTML += `<div>Bot: ${data.response}</div>`;
    chatbox.scrollTop = chatbox.scrollHeight;  // Scroll to the bottom
}
