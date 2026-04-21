from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)


def embed_chunks(chunks):
    if len(chunks) == 0:
        return []

    texts = []
    for c in chunks:
        if isinstance(c, dict) and "chunk" in c:
            texts.append(c["chunk"])
        else:
            texts.append(str(c))

    return model.encode(texts)


def embed_query(query):
    return model.encode([query])[0]