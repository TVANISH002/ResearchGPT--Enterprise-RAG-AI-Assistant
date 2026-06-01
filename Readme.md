# 🔍 ResearchGPT — Production-Style RAG System for Research Papers

![ResearchGPT CI](https://github.com/TVANISH002/ResearchGPT--Enterprise-RAG-AI-Assistant/actions/workflows/ci.yml/badge.svg)


A modular Retrieval-Augmented Generation (RAG) system that transforms research papers into a grounded question-answering engine — built for scalable corpus indexing, low-latency retrieval, and hallucination-resistant generation.

---

## 🚀 Problem Statement

LLMs often generate fluent but ungrounded answers on long documents.  
This system solves that by grounding every response in retrieved context from a curated research corpus.

---

## 🏗️ Architecture

### Ingestion
- PDF parsing using PyPDF2
- Handles multi-page research papers

### Chunking
- Fixed-size chunking with overlap
- Chunk size and overlap iteratively tuned for retrieval recall

### Embeddings
- Model: all-MiniLM-L6-v2
- Lightweight + fast, optimized for semantic similarity

### Vector Store
- FAISS (IndexFlatL2)
- Efficient similarity search across large corpora

### Retrieval
- Top-K similarity search
- Top-K tuned across multiple evaluation rounds for relevance vs latency

### Generation
- Local HuggingFace (optional)
- Groq API (recommended) for low-latency inference

---

## ⚙️ Key Design Decisions

- RAG over fine-tuning → dynamic, updatable, and cheaper
- FAISS → fast local retrieval at scale
- MiniLM → efficient embeddings without sacrificing quality
- Strict retrieval-grounded prompting → hallucination mitigation
- Modular layers → clean separation of ingestion, retrieval, reasoning, and serving

---

## 📊 Evaluation

Retrieval relevance was measured and iteratively improved through:
- Chunk size and overlap tuning
- Top-K retrieval parameter optimization
- Corpus expansion with domain-aligned research papers (RAG, FAISS, BM25, LoRA, retrieval evaluation)

Evaluation layer includes corpus statistics, retrieval benchmarking, and grounding checks to improve answer traceability.

Corpus designed to scale to **10,000+ chunks** for enterprise-grade retrieval coverage.

---

## ⚡ Performance

| Component | Optimization |
|---|---|
| Retrieval | FAISS index |
| Prompt | Reduced top-K |
| LLM | Groq API for low latency |
| Backend | FastAPI for production-ready serving |

---

## 📁 Project Structure

```
app/
├── ingestion/
├── retrieval/
├── generation/
├── evaluation/
├── config.py
└── main.py

frontend/
└── streamlitapp.py
```

---

## ⚙️ Setup

### Environment

```bash
uv venv --python 3.11
.venv\Scripts\activate
```

### Install

```bash
uv pip install -r requirements.txt
```

---

## ▶️ Run

### Backend

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
streamlit run frontend/streamlitapp.py
```

---

## 🧪 Usage

1. Upload a PDF
2. Ask a question
3. System retrieves relevant chunks
4. LLM generates grounded answer

---

## 🧠 Example Output

User question:

```text
What is Retrieval-Augmented Generation?
```

Example response:

```
Summary:
Retrieval-Augmented Generation (RAG) combines a language model with retrieved external context from a document corpus.

Method:
The system retrieves relevant document chunks from the FAISS vector index and passes those chunks to the LLM as grounded context.

Key Findings:
- RAG combines parametric language generation with non-parametric retrieval.
- Retrieved context helps produce more factual and specific answers.
- The answer is generated from source chunks rather than relying only on model memory.

Limitations:
Answer quality depends on the quality of retrieved chunks, corpus coverage, and retrieval configuration.

Conclusion:
RAG improves research-paper question answering by grounding LLM responses in retrieved evidence.
```

Example retrieved source metadata:

```json
{
  "retrieved_sources": [
    {
      "source": "Rag.pdf",
      "chunk_id": 2,
      "distance": 0.76
    },
    {
      "source": "Rag.pdf",
      "chunk_id": 0,
      "distance": 0.78
    }
  ]
}
```

---

## 🚀 Future Work

- LoRA fine-tuning
- Hybrid retrieval (BM25 + vector)
- Citation grounding
- Multi-document reasoning