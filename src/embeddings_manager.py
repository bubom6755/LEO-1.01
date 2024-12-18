import re
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

class EmbeddingsManager:
    def __init__(self, collection_name="legal_chunks", host="localhost", port=6333):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self._init_collection()

    def _init_collection(self):
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
        except Exception:
            print("Collection already exists. Skipping creation.")

    def index_chunks(self, chunks: list):
        points = []
        for i, chunk in enumerate(chunks):
            vector = self.model.encode(chunk).tolist()
            points.append(PointStruct(id=i, vector=vector, payload={"content": chunk}))
            yield i
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query: str, top_k: int = 3):
        query_vector = self.model.encode(query).tolist()
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
        )
        return [(res.payload["content"], res.score) for res in results]

    def search_by_keyword(self, query: str, raw_text: str):
        """
        Recherche par mots-clés pour les questions simples comme "titre" ou "chapitre".
        """
        if "titre" in query.lower() or "chapitre" in query.lower():
            match = re.search(r"^(CHAPITRE\s+\d+.*?)\n", raw_text, re.MULTILINE | re.IGNORECASE)
            return match.group(1) if match else "Aucun titre trouvé."
        return None
