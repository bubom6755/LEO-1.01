import re

def split_text(text, max_length=500):
    """
    Découpe le texte en chunks en respectant les titres, chapitres et sections.
    """
    chunks = []
    current_chunk = ""

    for line in text.split("\n"):
        # Détecter les titres ou chapitres
        if re.match(r"^\s*(CHAPITRE\s+\d+|TITRE\s+\d+|SECTION\s+\d+)", line, re.IGNORECASE):
            if current_chunk:  # Sauvegarder le chunk actuel
                chunks.append(current_chunk)
            current_chunk = line + "\n"  # Commence un nouveau chunk
        else:
            if len(current_chunk) + len(line) < max_length:
                current_chunk += line + "\n"
            else:
                chunks.append(current_chunk)
                current_chunk = line + "\n"

    if current_chunk:
        chunks.append(current_chunk)

    print(f"Nombre de chunks générés : {len(chunks)}")
    return chunks
