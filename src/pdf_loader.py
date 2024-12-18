import PyPDF2

def load_pdf(pdf_path: str) -> str:
    """
    Charge et extrait tout le texte d'un fichier PDF.
    """
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text
