from sentence_transformers import SentenceTransformer

from app.config import EMBEDDING_MODEL


_model = None


def get_embedding_model():
    """
    Load the embedding model only once.
    """
    global _model

    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)

    return _model


def embed_texts(texts: list[str]):
    """
    Convert text into embedding vectors.

    Input:
        ["text one", "text two"]

    Output:
        numpy array of embeddings
    """
    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings