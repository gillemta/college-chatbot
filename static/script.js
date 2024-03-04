document.addEventListener('DOMContentLoaded', function() {
    loadInitialMessages();

    document.getElementById('messageForm').addEventListener('submit', function(event) {
        event.preventDefault();

        var userInput = document.getElementById('userInput').value.trim();
        if (userInput !== "") {
            sendMessage(userInput);
            document.getElementById("userInput").value = "";
        }
    });
});

function loadInitialMessages() {
    fetch('/initial_messages')
    .then(response => response.json())
    .then(data => {
        data.messages.forEach(message => {
            appendMessage("incoming", message);
        });
    })
    .catch(error => console.error('Error:', error));
}

function sendMessage(userInput) {
    appendMessage("outgoing", userInput);
    fetch('/message', {
        method: 'POST',
        body: new URLSearchParams({userInput: userInput}),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        appendMessage("incoming", data.response);
        if (data.response.includes("Here's a summary of your interaction")) {
            getSummary();
        }
        if (data.response.includes("Thank you for providing your information")) {
            appendMessage("incoming", "If you would like to end this chat and display the summary, then type in 'END' in the chat.")
        }
    })
    .catch(error => console.error('Error:', error));
}

function getSummary() {
    fetch('/summary')
    .then(response => response.json())
    .then(data => {

        var summaryMessage = "User Information:<br>";
        summaryMessage += `- First Name: ${data.user_information.first_name}<br>`;
        summaryMessage += `- Last Name: ${data.user_information.last_name}<br>`;
        summaryMessage += `- Email Address: ${data.user_information.email}<br><br>`;

        summaryMessage += "Chatbot Creator Information:<br>";
        summaryMessage += `- First Name: ${data.chatbot_creator_information.first_name}<br>`;
        summaryMessage += `- Last Name: ${data.chatbot_creator_information.last_name}<br>`;
        summaryMessage += `- School Email Address: ${data.chatbot_creator_information.school_email}<br>`;

        appendMessage("incoming", summaryMessage);
    })
    .catch(error => console.error('Error:', error));
}



function appendMessage(sender, message) {
    var chatContent = document.getElementById("chatContent");
    var messageElement = document.createElement("div");
    messageElement.classList.add(sender === "outgoing" ? "outgoing-message" : "incoming-message");
    messageElement.innerHTML = message;
    chatContent.appendChild(messageElement);

    setTimeout(function() {
        messageElement.classList.add("show");
    }, 1000);
}