from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def embed_chunks(chunks):
    return model.encode(chunks)

def embed_query(query):
    return model.encode([query])[0]