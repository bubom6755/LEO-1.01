import sqlite3

class DBManager:
    def __init__(self, db_path="data/qna.db"):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        cursor = self.connection.cursor()
        # Table temporaire
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS temp_qna (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            response TEXT NOT NULL
        )
        """)
        # Table validée
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS validated_qna (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            response TEXT NOT NULL
        )
        """)
        self.connection.commit()

    def add_temp_qna(self, question, response):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO temp_qna (question, response) VALUES (?, ?)", (question, response))
        self.connection.commit()

    def get_temp_qna(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM temp_qna")
        return cursor.fetchall()

    def validate_qna(self, qna_id):
        cursor = self.connection.cursor()
        # Récupérer la question/réponse
        cursor.execute("SELECT question, response FROM temp_qna WHERE id=?", (qna_id,))
        qna = cursor.fetchone()
        if qna:
            # Ajouter à la table validée
            cursor.execute("INSERT INTO validated_qna (question, response) VALUES (?, ?)", qna)
            # Supprimer de la table temporaire
            cursor.execute("DELETE FROM temp_qna WHERE id=?", (qna_id,))
            self.connection.commit()
            return True
        return False

    def delete_temp_qna(self, qna_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM temp_qna WHERE id=?", (qna_id,))
        self.connection.commit()

    def search_validated_qna(self, query):
        cursor = self.connection.cursor()
        cursor.execute("SELECT question, response FROM validated_qna")
        results = cursor.fetchall()
        # Recherche approximative dans les questions validées
        for question, response in results:
            if query.lower() in question.lower():
                return response
        return None
