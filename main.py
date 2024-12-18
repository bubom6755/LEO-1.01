from src.pdf_loader import load_pdf
from src.text_splitter import split_text
from src.embeddings_manager import EmbeddingsManager
from src.llm_interface import LLMInterface
from src.progress_bar import show_progress

def main():
    pdf_path = "data/document.pdf"
    embeddings_manager = EmbeddingsManager()
    llm = LLMInterface(model_name="llama3")

    print("Extraction du PDF...")
    raw_text = load_pdf(pdf_path)

    print("Découpage du texte...")
    chunks = split_text(raw_text)

    print("Indexation des embeddings...")
    show_progress(embeddings_manager.index_chunks(chunks))

    print("\nChatbot prêt ! Posez vos questions (tapez 'exit' pour quitter).")
    while True:
        query = input("Question : ")
        if query.lower() == "exit":
            print("À bientôt !")
            break
        response, context = llm.answer(query, embeddings_manager, raw_text)

        print("\nRéponse :", response)
        if context:
            print("\nArticles pertinents :")
            for article, _ in context:
                print("-", article[:200])  # Affiche un extrait des articles

if __name__ == "__main__":
    main()
