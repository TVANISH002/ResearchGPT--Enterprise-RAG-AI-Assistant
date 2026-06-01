import os
import pickle

import faiss
import numpy as np

from app.config import VECTOR_DIR


class FAISSVectorStore:
    """
    Local FAISS vector store for semantic search.
    """

    def __init__(self):
        self.index = None
        self.chunks = []
        self.dimension = None

    def build(self, embeddings, chunks: list[dict]):
        """
        Build FAISS index from embeddings and chunk metadata.
        """
        embeddings = np.array(embeddings).astype("float32")

        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings)

        self.chunks = chunks

    def search(self, query_embedding, top_k: int = 5) -> list[dict]:
        """
        Search top-k similar chunks.
        """
        if self.index is None:
            raise ValueError("FAISS index is not built yet.")

        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for rank, idx in enumerate(indices[0]):
            if idx < len(self.chunks):
                chunk = self.chunks[idx].copy()
                chunk["distance"] = float(distances[0][rank])
                results.append(chunk)

        return results

    def save(self):
        """
        Save FAISS index and chunk metadata.
        """
        if self.index is None:
            raise ValueError("No FAISS index available to save.")

        index_path = os.path.join(VECTOR_DIR, "researchgpt.index")
        chunks_path = os.path.join(VECTOR_DIR, "chunks.pkl")

        faiss.write_index(self.index, index_path)

        with open(chunks_path, "wb") as file:
            pickle.dump(self.chunks, file)

    def load(self):
        """
        Load FAISS index and chunk metadata.
        """
        index_path = os.path.join(VECTOR_DIR, "researchgpt.index")
        chunks_path = os.path.join(VECTOR_DIR, "chunks.pkl")

        if not os.path.exists(index_path):
            raise FileNotFoundError("FAISS index file not found.")

        if not os.path.exists(chunks_path):
            raise FileNotFoundError("Chunk metadata file not found.")

        self.index = faiss.read_index(index_path)

        with open(chunks_path, "rb") as file:
            self.chunks = pickle.load(file)