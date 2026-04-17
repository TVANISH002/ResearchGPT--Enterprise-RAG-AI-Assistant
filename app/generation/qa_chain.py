from transformers import pipeline
from app.config import LLM_MODEL

generator = pipeline("text2text-generation", model=LLM_MODEL)

def generate_answer(context_chunks, query):
    context = "\n".join(context_chunks)

    prompt = f"""
    Answer the question based only on the context below.

    Context:
    {context}

    Question:
    {query}
    """

    result = generator(prompt, max_length=256, do_sample=False)
    return result[0]['generated_text']