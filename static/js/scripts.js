document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');

    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const message = userInput.value.trim();
        if (message === '') return;

        // Display user's message
        appendMessage('user', message);
        userInput.value = '';

        // Send message to the backend
        fetch('/bot/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Display assistant's response
            appendMessage('assistant', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('assistant', 'An error occurred. Please try again.');
        });
    });

    function renderMarkdown(text) {
        const rawHtml = marked.parse(text);
        return DOMPurify.sanitize(rawHtml);
    }

    
function appendMessage(sender, message) {
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message', sender);

    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.innerHTML = renderMarkdown(message);

    messageContainer.appendChild(messageContent);
    chatWindow.appendChild(messageContainer);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

    const uploadButton = document.getElementById('upload-button');
    const logFileInput = document.getElementById('log-file-input');

    uploadButton.addEventListener('click', function () {
        logFileInput.click();
    });

    logFileInput.addEventListener('change', function () {
        const file = logFileInput.files[0];
        if (file) {
            // Display the file name in the chat window
            appendMessage('user', `Uploaded file: ${file.name}`);

            const formData = new FormData();
            formData.append('file', file);

            fetch('/bot/upload', {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    appendMessage('assistant', data.analysis);
                })
                .catch(error => {
                    console.error('Error:', error);
                    appendMessage('assistant', 'An error occurred while uploading the file. Please try again.');
                });
        }
    });
});

const clearChatButton = document.getElementById('clear-chat');
clearChatButton.addEventListener('click', function () {
    fetch('/bot/clear', { method: 'POST' })
        .then(() => {
            chatWindow.innerHTML = '';
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

// function validateFileSize(input) {
//     const file = input.files[0];
//     const maxSize = 512 * 1024; 

//     if (file && file.size > maxSize) {
//         alert("During demo session, maximum file size is limited to 512 KB.");
//         input.value = ""; 
//     }
// }





