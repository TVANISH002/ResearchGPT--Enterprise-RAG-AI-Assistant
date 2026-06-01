from groq import Groq

from app.config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    MAX_NEW_TOKENS,
    TEMPERATURE,
    TOP_P,
    REQUIRED_SECTIONS
)


def format_retrieved_context(retrieved_chunks: list[dict]) -> str:
    context_blocks = []

    for chunk in retrieved_chunks:
        source = chunk.get("source", "unknown")
        chunk_id = chunk.get("chunk_id", "unknown")
        text = chunk.get("text", "")

        block = f"[Source: {source} | Chunk: {chunk_id}]\n{text}"
        context_blocks.append(block)

    return "\n\n".join(context_blocks)


def build_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    context = format_retrieved_context(retrieved_chunks)

    sections = "\n".join([f"- {section}" for section in REQUIRED_SECTIONS])

    prompt = f"""
You are ResearchGPT, a research-paper question answering assistant.

Your task:
Answer the user's question using ONLY the retrieved research-paper context.

Rules:
1. Do not use outside knowledge.
2. If the context is insufficient, say:
   "I could not find enough evidence in the retrieved research context."
3. Keep the answer clear and structured.
4. Mention evidence from the retrieved context where useful.
5. Do not invent citations, page numbers, or claims.

Retrieved Context:
{context}

Question:
{question}

Return the answer using these sections:
{sections}
"""

    return prompt.strip()


def generate_answer(question: str, retrieved_chunks: list[dict]) -> dict:
    if not GROQ_API_KEY:
        return {
            "error": "GROQ_API_KEY is missing. Add it to your .env file.",
            "question": question
        }

    prompt = build_prompt(question, retrieved_chunks)

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a grounded research-paper QA assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_NEW_TOKENS,
        top_p=TOP_P
    )

    answer_text = response.choices[0].message.content

    return {
        "answer": answer_text,
        "model": GROQ_MODEL,
        "retrieved_context_count": len(retrieved_chunks)
    }