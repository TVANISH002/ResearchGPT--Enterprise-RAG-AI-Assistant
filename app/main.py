import os
import shutil

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.config import UPLOAD_DIR, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K
from app.ingestion.pdf_loader import load_pdfs
from app.ingestion.chunker import chunk_documents
from app.retrieval.retriever import ResearchRetriever
from app.generation.qa_chain import generate_answer


app = FastAPI(
    title="ResearchGPT API",
    description="Production-style RAG system for research-paper question answering.",
    version="1.0.0"
)

retriever = ResearchRetriever()
index_ready = False


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "project": "ResearchGPT",
        "message": "ResearchGPT API is running.",
        "pipeline": "PDF Upload → Text Extraction → Chunking → Embedding → FAISS → Retrieval → LLM Answer"
    }


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "PDF uploaded successfully.",
        "file_name": file.filename,
        "saved_to": file_path
    }


@app.post("/build-index")
def build_index():
    global index_ready

    pdf_texts = load_pdfs(UPLOAD_DIR)

    if not pdf_texts:
        raise HTTPException(
            status_code=404,
            detail="No PDFs found. Please upload a research paper first."
        )

    chunks = chunk_documents(
        pdf_texts=pdf_texts,
        chunk_size=CHUNK_SIZE,
        overlap=CHUNK_OVERLAP
    )

    retriever.build_index(chunks)
    retriever.save_index()

    index_ready = True

    return {
        "message": "Index built successfully.",
        "documents_processed": len(pdf_texts),
        "chunks_generated": len(chunks),
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "top_k": TOP_K
    }


@app.post("/ask")
def ask_question(request: QueryRequest):
    global index_ready

    if not index_ready:
        try:
            retriever.load_index()
            index_ready = True
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Index not found. Please upload PDFs and run /build-index first."
            )

    retrieved_chunks = retriever.retrieve(
        query=request.question,
        top_k=TOP_K
    )

    answer = generate_answer(
        question=request.question,
        retrieved_chunks=retrieved_chunks
    )

    return {
        "question": request.question,
        "retrieved_sources": [
            {
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "distance": chunk.get("distance")
            }
            for chunk in retrieved_chunks
        ],
        "answer": answer
    }