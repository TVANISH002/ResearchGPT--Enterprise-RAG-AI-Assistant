from fastapi import FastAPI, UploadFile, File
from helper import log_info, log_error

from app.ingestion.loader import save_pdf, extract_text
from app.ingestion.splitter import split_text
from app.ingestion.embedder import embed_chunks, embed_query

from app.retrieval.vector_store import save_index, load_index
from app.retrieval.retriever import retrieve

from app.generation.qa_chain import generate_answer

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        path = save_pdf(file)
        log_info(f"Uploaded: {file.filename}")

        text = extract_text(path)
        chunks = split_text(text)

        embeddings = embed_chunks(chunks)
        save_index(chunks, embeddings)

        return {"message": "PDF processed successfully"}

    except Exception as e:
        log_error(str(e))
        return {"error": str(e)}


@app.post("/query")
async def query(q: str):
    try:
        index, chunks = load_index()

        q_vec = embed_query(q)
        top_chunks = retrieve(q_vec, index, chunks)

        answer = generate_answer(top_chunks, q)

        log_info(f"Query: {q}")

        return {"answer": answer}

    except Exception as e:
        log_error(str(e))
        return {"error": str(e)}