import os

def file_exists(path: str) -> bool:
    """
    Vérifie si un fichier existe.
    """
    return os.path.exists(path)
