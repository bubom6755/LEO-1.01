document.getElementById("send-btn").addEventListener("click", sendMessage);
document
  .getElementById("user-input")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
  });

function sendMessage() {
  const userInput = document.getElementById("user-input");
  const messageBox = document.getElementById("messages");
  const question = userInput.value.trim();

  if (!question) return;

  // Afficher le message de l'utilisateur
  messageBox.innerHTML += `<div class="message user-message">${question}</div>`;

  // Barre de progression
  messageBox.innerHTML += `
        <div id="progress-bar-container">
            <div class="progress-bar"></div>
        </div>
    `;

  // Envoyer la requête à Flask
  fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: question }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Supprimer la barre de progression
      const progressBar = document.getElementById("progress-bar-container");
      if (progressBar) progressBar.remove();

      // Afficher la réponse du bot
      const botMessage = `
            <div class="message bot-message">
                <p>${data.response}</p>
                ${
                  data.context.length > 0
                    ? `
                    <button class="toggle-articles">🔎 Voir les articles</button>
                    <div class="articles hidden">
                        ${data.context
                          .map((article) => `<p>${article}</p>`)
                          .join("")}
                    </div>
                `
                    : ""
                }
            </div>
        `;
      messageBox.innerHTML += botMessage;

      // Ajouter le toggle pour afficher/masquer les articles
      document.querySelectorAll(".toggle-articles").forEach((button) => {
        button.addEventListener("click", function () {
          this.nextElementSibling.classList.toggle("hidden");
        });
      });

      messageBox.scrollTop = messageBox.scrollHeight;
    });

  userInput.value = "";
}
