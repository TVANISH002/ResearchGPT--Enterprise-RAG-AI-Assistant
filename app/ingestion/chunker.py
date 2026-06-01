def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """
    Split long text into overlapping chunks.
    """
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def chunk_documents(
    pdf_texts: dict,
    chunk_size: int = 500,
    overlap: int = 100
) -> list[dict]:
    """
    Convert multiple PDF texts into structured chunks.
    """
    all_chunks = []

    for file_name, text in pdf_texts.items():
        chunks = chunk_text(
            text=text,
            chunk_size=chunk_size,
            overlap=overlap
        )

        for index, chunk in enumerate(chunks):
            all_chunks.append({
                "source": file_name,
                "chunk_id": index,
                "text": chunk
            })

    return all_chunks