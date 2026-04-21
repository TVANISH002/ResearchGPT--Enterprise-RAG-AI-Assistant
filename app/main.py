from fastapi import FastAPI, UploadFile, File
from app.helper import log_info, log_error

from app.ingestion.loader import save_pdf, extract_text
from app.ingestion.splitter import split_text
from app.ingestion.embedder import embed_chunks, embed_query

from app.retrieval.vector_store import save_index, load_index
from app.retrieval.retriever import retrieve
from app.retrieval.query_rewriter import rewrite_query

from app.generation.qa_chain import generate_answer

app = FastAPI(title="ResearchGPT API")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        path = save_pdf(file)
        log_info(f"Uploaded: {file.filename}")

        text = extract_text(path)
        raw_chunks = split_text(text)

        chunks = [
            {"chunk": chunk, "pdf": file.filename, "page": "unknown"}
            for chunk in raw_chunks
        ]

        embeddings = embed_chunks(chunks)
        save_index(chunks, embeddings)

        return {
            "message": "PDF processed successfully",
            "num_chunks": len(chunks),
            "filename": file.filename
        }

    except Exception as e:
        log_error(str(e))
        return {"error": str(e)}


@app.post("/query")
async def query(q: str, mode: str = "base"):
    try:
        index, chunks = load_index()

        rewritten_q = rewrite_query(q)
        q_vec = embed_query(rewritten_q)
        top_chunks = retrieve(q_vec, index, chunks)

        answer = generate_answer(top_chunks, rewritten_q, mode=mode)

        log_info(f"Query: {q} | Mode: {mode}")

        return {
            "query": q,
            "rewritten_query": rewritten_q,
            "mode": mode,
            "retrieved_chunks": top_chunks,
            "answer": answer
        }

    except Exception as e:
        log_error(str(e))
        return {"error": str(e)}