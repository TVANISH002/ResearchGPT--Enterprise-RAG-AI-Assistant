test_cases = [
    {
        "question": "What is transformer architecture?",
        "expected_keywords": ["transformer", "attention", "encoder", "decoder"]
    },
    {
        "question": "How does self-attention work?",
        "expected_keywords": ["self-attention", "attention", "tokens", "sequence"]
    },
    {
        "question": "Why are transformers better than RNNs?",
        "expected_keywords": ["parallel", "attention", "rnn", "sequence"]
    },
    {
        "question": "What is the role of the encoder?",
        "expected_keywords": ["encoder", "input", "representation", "context"]
    },
    {
        "question": "What is the role of the decoder?",
        "expected_keywords": ["decoder", "output", "generation", "sequence"]
    },
    {
        "question": "What is BERT?",
        "expected_keywords": ["bert", "bidirectional", "transformer", "pretraining"]
    },
    {
        "question": "How is BERT trained?",
        "expected_keywords": ["masked", "language", "pretraining", "bert"]
    },
    {
        "question": "What NLP tasks can BERT perform?",
        "expected_keywords": ["classification", "question answering", "nlp", "bert"]
    },
    {
        "question": "Why is BERT bidirectional?",
        "expected_keywords": ["bidirectional", "context", "left", "right"]
    },
    {
        "question": "How is BERT fine-tuned?",
        "expected_keywords": ["fine-tuning", "downstream", "task", "bert"]
    },
    {
        "question": "What are sentence embeddings?",
        "expected_keywords": ["embeddings", "vector", "semantic", "representation"]
    },
    {
        "question": "Why are embeddings important?",
        "expected_keywords": ["semantic", "vector", "similarity", "retrieval"]
    },
    {
        "question": "What is embedding similarity?",
        "expected_keywords": ["cosine", "similarity", "embedding", "vector"]
    },
    {
        "question": "What is semantic search?",
        "expected_keywords": ["semantic", "search", "meaning", "retrieval"]
    },
    {
        "question": "How are embeddings generated?",
        "expected_keywords": ["embedding", "model", "vector", "representation"]
    },
    {
        "question": "What is FAISS?",
        "expected_keywords": ["faiss", "similarity", "search", "vectors"]
    },
    {
        "question": "Why use FAISS in RAG systems?",
        "expected_keywords": ["faiss", "retrieval", "vector", "search"]
    },
    {
        "question": "What types of indexes does FAISS support?",
        "expected_keywords": ["flat", "ivf", "hnsw", "index"]
    },
    {
        "question": "How does FAISS improve retrieval speed?",
        "expected_keywords": ["search", "efficient", "vector", "retrieval"]
    },
    {
        "question": "Can FAISS run on GPU?",
        "expected_keywords": ["gpu", "faiss", "acceleration", "vector"]
    },
    {
        "question": "What is retrieval augmented generation?",
        "expected_keywords": ["rag", "retrieval", "generation", "context"]
    },
    {
        "question": "Why use RAG instead of pure LLMs?",
        "expected_keywords": ["retrieval", "knowledge", "context", "hallucination"]
    },
    {
        "question": "How does RAG reduce hallucinations?",
        "expected_keywords": ["retrieval", "grounded", "context", "hallucination"]
    },
    {
        "question": "What are the components of a RAG pipeline?",
        "expected_keywords": ["retrieval", "generation", "embedding", "index"]
    },
    {
        "question": "How does chunking affect retrieval?",
        "expected_keywords": ["chunking", "retrieval", "context", "chunks"]
    },
    {
        "question": "Why use chunk overlap?",
        "expected_keywords": ["overlap", "chunk", "context", "continuity"]
    },
    {
        "question": "What is recursive chunking?",
        "expected_keywords": ["recursive", "chunking", "splitter", "documents"]
    },
    {
        "question": "How do chunk size and overlap impact retrieval?",
        "expected_keywords": ["chunk", "overlap", "retrieval", "context"]
    },
    {
        "question": "What is metadata filtering?",
        "expected_keywords": ["metadata", "filtering", "retrieval", "documents"]
    },
    {
        "question": "Why is metadata useful in retrieval?",
        "expected_keywords": ["metadata", "search", "filter", "retrieval"]
    },
    {
        "question": "What is prompt engineering?",
        "expected_keywords": ["prompt", "instructions", "llm", "generation"]
    },
    {
        "question": "What is few-shot prompting?",
        "expected_keywords": ["few-shot", "examples", "prompt"]
    },
    {
        "question": "What is chain-of-thought prompting?",
        "expected_keywords": ["chain", "reasoning", "steps", "prompt"]
    },
    {
        "question": "What is ReAct prompting?",
        "expected_keywords": ["reasoning", "acting", "tools", "react"]
    },
    {
        "question": "How does prompt design affect answers?",
        "expected_keywords": ["prompt", "quality", "response", "generation"]
    },
    {
        "question": "What is fine-tuning?",
        "expected_keywords": ["fine-tuning", "training", "model", "task"]
    },
    {
        "question": "Why fine-tune a language model?",
        "expected_keywords": ["adaptation", "task", "fine-tuning", "model"]
    },
    {
        "question": "What is LoRA?",
        "expected_keywords": ["lora", "adapter", "fine-tuning", "parameters"]
    },
    {
        "question": "How does parameter-efficient fine-tuning work?",
        "expected_keywords": ["parameter", "efficient", "lora", "fine-tuning"]
    },
    {
        "question": "What is PEFT?",
        "expected_keywords": ["peft", "fine-tuning", "efficient", "adapter"]
    },
    {
        "question": "What are the limitations of transformer models?",
        "expected_keywords": ["limitations", "transformer", "context", "computation"]
    },
    {
        "question": "What challenges exist in RAG systems?",
        "expected_keywords": ["retrieval", "hallucination", "latency", "rag"]
    },
    {
        "question": "What causes hallucinations in LLMs?",
        "expected_keywords": ["hallucination", "incorrect", "generation", "facts"]
    },
    {
        "question": "How can hallucinations be reduced?",
        "expected_keywords": ["grounding", "retrieval", "context", "verification"]
    },
    {
        "question": "Why is evaluation important in RAG systems?",
        "expected_keywords": ["evaluation", "retrieval", "quality", "benchmark"]
    },
    {
        "question": "How do we evaluate retrieval quality?",
        "expected_keywords": ["retrieval", "precision", "recall", "evaluation"]
    },
    {
        "question": "What is cosine similarity?",
        "expected_keywords": ["cosine", "similarity", "vector", "embedding"]
    },
    {
        "question": "How do vector databases work?",
        "expected_keywords": ["vector", "database", "embedding", "retrieval"]
    },
    {
        "question": "What is document grounding?",
        "expected_keywords": ["grounding", "documents", "context", "retrieval"]
    },
    {
        "question": "What is the workflow of a research paper RAG system?",
        "expected_keywords": ["ingestion", "retrieval", "generation", "evaluation"]
    }
]



if __name__ == "__main__":
    print(f"Total benchmark questions: {len(test_cases)}")