import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "papers")
VECTOR_DIR = os.path.join(BASE_DIR, "vector_store")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# -----------------------------
# Chunking / Retrieval
# -----------------------------
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))
TOP_K = int(os.getenv("TOP_K", 2))

# -----------------------------
# Embeddings
# -----------------------------
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# -----------------------------
# Generation
# -----------------------------
BASE_MODEL_NAME = os.getenv("BASE_MODEL_NAME", "distilgpt2")
FINETUNED_ADAPTER_PATH = os.getenv("FINETUNED_ADAPTER_PATH", "outputs/fine_tuned_lora_model")

MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", 150))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))
TOP_P = float(os.getenv("TOP_P", 0.9))

# -----------------------------
# Structured output sections
# -----------------------------
REQUIRED_SECTIONS = [
    "Summary",
    "Method",
    "Key Findings",
    "Limitations",
    "Conclusion",
]