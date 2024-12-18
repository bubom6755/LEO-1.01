from flask import Flask, request, jsonify, render_template, redirect, url_for
from src.pdf_loader import load_pdf
from src.text_splitter import split_text
from src.embeddings_manager import EmbeddingsManager
from src.llm_interface import LLMInterface
from src.progress_bar import show_progress
from src.db_manager import DBManager

app = Flask(__name__)

# Initialisation de la base de données
db_manager = DBManager()

# Initialisation des composants
embeddings_manager = EmbeddingsManager()
llm = LLMInterface(model_name="llama3")

# Préparation des données
pdf_path = "data/document.pdf"
print("Extraction du PDF...")
raw_text = load_pdf(pdf_path)

print("Découpage du texte...")
chunks = split_text(raw_text)

print("Indexation des embeddings...")
for _ in embeddings_manager.index_chunks(chunks):
    pass
print("Indexation terminée.")


@app.route("/")
def index():
    """
    Page principale de l'interface utilisateur.
    """
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    """
    API pour poser une question au chatbot.
    """
    user_question = request.json.get("question", "")
    if not user_question:
        return jsonify({"response": "Veuillez poser une question valide.", "context": []})

    # Vérification dans la BDD validée
    validated_response = db_manager.search_validated_qna(user_question)
    if validated_response:
        return jsonify({"response": validated_response, "context": []})

    # Réponse de l'agent
    response, context = llm.answer(user_question, embeddings_manager, raw_text)

    # Sauvegarder dans la table temporaire
    db_manager.add_temp_qna(user_question, response)

    # Structurer la réponse pour l'interface
    return jsonify({
        "response": response,
        "context": [article for article, _ in context]
    })


@app.route("/admin", methods=["GET", "POST"])
def admin():
    """
    Page d'administration pour valider ou supprimer des questions/réponses.
    """
    if request.method == "POST":
        action = request.form.get("action")
        qna_id = int(request.form.get("qna_id"))
        if action == "validate":
            db_manager.validate_qna(qna_id)
        elif action == "delete":
            db_manager.delete_temp_qna(qna_id)
        return redirect(url_for("admin"))

    # Récupérer toutes les questions/réponses en attente
    temp_qna = db_manager.get_temp_qna()
    return render_template("admin.html", temp_qna=temp_qna)


if __name__ == "__main__":
    app.run(debug=True)
