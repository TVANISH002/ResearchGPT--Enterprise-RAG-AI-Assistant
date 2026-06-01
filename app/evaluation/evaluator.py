import re


def normalize_text(text: str) -> str:
    """
    Lowercase text and normalize spaces.
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def keyword_match_score(text: str, expected_keywords: list[str]) -> float:
    """
    Calculate keyword match score.

    Example:
        expected_keywords = ["rag", "retrieval", "generation", "context"]

        If retrieved text contains 3 out of 4 keywords:
        score = 3 / 4 = 0.75
    """
    text = normalize_text(text)

    if not expected_keywords:
        return 0.0

    matched = 0

    for keyword in expected_keywords:
        if keyword.lower() in text:
            matched += 1

    return matched / len(expected_keywords)


def grounding_score(answer: str, retrieved_context: str) -> float:
    """
    Simple grounding score based on word overlap between answer and retrieved context.
    """
    answer_words = set(normalize_text(answer).split())
    context_words = set(normalize_text(retrieved_context).split())

    if not answer_words:
        return 0.0

    overlap = answer_words.intersection(context_words)

    return len(overlap) / len(answer_words)


def classify_grounding(score: float) -> str:
    """
    Classify answer grounding quality.
    """
    if score >= 0.45:
        return "High grounding"
    elif score >= 0.25:
        return "Medium grounding"
    return "Low grounding"