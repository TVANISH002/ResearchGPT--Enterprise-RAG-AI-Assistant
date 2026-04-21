import numpy as np
from app.config import TOP_K

def retrieve(query_embedding, index, chunks):
    D, I = index.search(
        np.array([query_embedding]).astype("float32"),
        TOP_K
    )
    return [chunks[i] for i in I[0]]