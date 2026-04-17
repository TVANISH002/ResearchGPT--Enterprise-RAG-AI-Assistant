import pickle

# Enhanced dummy chunks simulating multiple PDFs and pages
chunks = [
    # PDF 1
    "Transformers are neural networks designed for sequential data. They use self-attention to process sequences in parallel.",
    "The encoder processes input sequences, while the decoder generates output sequences step-by-step.",
    "Attention heads allow the model to focus on different parts of the sequence simultaneously.",
    
    # PDF 2
    "BERT (Bidirectional Encoder Representations from Transformers) pre-trains deep bidirectional representations.",
    "BERT is fine-tuned for downstream NLP tasks like sentiment analysis and question answering.",
    "Fine-tuning requires relatively small datasets due to pre-trained knowledge.",
    
    # PDF 3
    "FAISS is a library for efficient similarity search of dense vectors, perfect for RAG pipelines.",
    "It supports flat, IVFFlat, and HNSW indices for various performance requirements.",
    "FAISS allows storing embeddings locally or mapping to GPU for acceleration.",
    
    # PDF 4
    "MiniLM embeddings are small yet effective sentence embeddings from HuggingFace Transformers.",
    "They are lightweight and fast, ideal for local RAG projects or prototypes.",
    "Embedding vectors are used for similarity search and retrieval in vector databases."
]

# Save to chunks.pkl inside vector_store
with open("vector_store/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)




metadata_chunks = [
    {"chunk": chunks[0], "pdf": "transformers_intro.pdf", "page": 1},
    {"chunk": chunks[1], "pdf": "transformers_intro.pdf", "page": 2},
    {"chunk": chunks[2], "pdf": "transformers_intro.pdf", "page": 3},
    {"chunk": chunks[3], "pdf": "bert_paper.pdf", "page": 1},
    {"chunk": chunks[4], "pdf": "bert_paper.pdf", "page": 2},
    {"chunk": chunks[5], "pdf": "bert_paper.pdf", "page": 3},
    {"chunk": chunks[6], "pdf": "faiss_guide.pdf", "page": 1},
    {"chunk": chunks[7], "pdf": "faiss_guide.pdf", "page": 2},
    {"chunk": chunks[8], "pdf": "faiss_guide.pdf", "page": 3},
    {"chunk": chunks[9], "pdf": "minilm_embeddings.pdf", "page": 1},
    {"chunk": chunks[10], "pdf": "minilm_embeddings.pdf", "page": 2},
    {"chunk": chunks[11], "pdf": "minilm_embeddings.pdf", "page": 3}
]

with open("vector_store/chunks.pkl", "wb") as f:
    pickle.dump(metadata_chunks, f)

print("Enhanced metadata chunks.pkl created successfully!")




print("Enhanced chunks.pkl created successfully!")