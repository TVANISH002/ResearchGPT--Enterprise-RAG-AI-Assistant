from sklearn.metrics.pairwise import cosine_similarity
from app.ingestion.embedder import model

def evaluate(predicted, expected):
    pred_vec = model.encode([predicted])
    exp_vec = model.encode([expected])

    score = cosine_similarity(pred_vec, exp_vec)[0][0]
    return score