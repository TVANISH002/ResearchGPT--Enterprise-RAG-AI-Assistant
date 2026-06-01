from app.ingestion.embedder import embed_texts
from app.retrieval.vector_store import FAISSVectorStore


class ResearchRetriever:
    """
    Handles embedding, indexing, saving, loading, and retrieval.
    """

    def __init__(self):
        self.vector_store = FAISSVectorStore()

    def build_index(self, chunks: list[dict]):
        """
        Build FAISS index from document chunks.
        """
        texts = [chunk["text"] for chunk in chunks]

        embeddings = embed_texts(texts)

        self.vector_store.build(
            embeddings=embeddings,
            chunks=chunks
        )

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Retrieve top-k chunks for a user query.
        """
        query_embedding = embed_texts([query])

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        return results

    def save_index(self):
        """
        Save FAISS index and metadata.
        """
        self.vector_store.save()

    def load_index(self):
        """
        Load FAISS index and metadata.
        """
        self.vector_store.load()