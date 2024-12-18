import requests
import src.db_manager as db_manager

class LLMInterface:
    def __init__(self, model_name="llama3", api_url="http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.api_url = api_url

    def answer(self, query: str, embeddings_manager, raw_text):
        # Étape 1 : Recherche par mots-clés pour questions simples
        keyword_response = embeddings_manager.search_by_keyword(query, raw_text)
        if keyword_response:
            return f"Réponse trouvée directement : {keyword_response}", []

        # Étape 2 : Recherche dans Qdrant et préparation du prompt
        context = embeddings_manager.search(query, top_k=3)
        context_text = "\n".join([chunk[:300] for chunk, _ in context])
        prompt = f"""
        Tu es un assistant juridique basé sur le règlement AI Act.
        Utilise uniquement le contexte suivant pour répondre :

        {context_text}

        Question : {query}

        Réponds de manière précise, concise et cite les articles pertinents si possible.
        """

        payload = {"model": self.model_name, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "Pas de réponse trouvée."), context
        except requests.exceptions.RequestException as e:
            return f"Erreur de requête : {e}", []

def answer(self, query: str, embeddings_manager, raw_text):
    # Étape 1 : Vérifier si une réponse validée existe
    validated_response = db_manager.search_validated_qna(query)
    context_text = validated_response if validated_response else ""

    # Étape 2 : Ajouter le contexte trouvé dans Qdrant
    context = embeddings_manager.search(query, top_k=3)
    for chunk, _ in context:
        context_text += "\n" + chunk[:300]

    # Étape 3 : Générer la réponse avec le LLM
    prompt = f"""
    Tu es un assistant juridique basé sur le règlement AI Act.
    Utilise uniquement le contexte suivant pour répondre :

    {context_text}

    Question : {query}

    Réponds de manière précise, concise et cite les articles pertinents si possible.
    """
    ...