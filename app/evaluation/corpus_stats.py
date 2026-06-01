from pathlib import Path
import json
from datetime import datetime

from app.config import UPLOAD_DIR, REPORT_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from app.ingestion.pdf_loader import extract_text_from_pdf, count_pdf_pages
from app.ingestion.chunker import chunk_text


def get_corpus_scale(total_chunks: int) -> str:
    """
    Classify corpus size for project reporting.
    """
    if total_chunks >= 10000:
        return "large"
    if total_chunks >= 1000:
        return "medium"
    return "sample"


def calculate_corpus_stats() -> dict:
    """
    Calculate corpus-level statistics from all PDFs inside the papers/ folder.

    Outputs:
    - number of documents
    - total pages
    - total characters
    - total chunks
    - chunk size
    - chunk overlap
    - per-document chunk count
    """
    papers_dir = Path(UPLOAD_DIR)
    pdf_files = sorted(list(papers_dir.glob("*.pdf")))

    document_stats = []
    total_pages = 0
    total_characters = 0
    total_chunks = 0

    for pdf_file in pdf_files:
        text = extract_text_from_pdf(str(pdf_file))

        chunks = chunk_text(
            text=text,
            chunk_size=CHUNK_SIZE,
            overlap=CHUNK_OVERLAP
        )

        page_count = count_pdf_pages(str(pdf_file))

        document_stats.append({
            "file_name": pdf_file.name,
            "pages": page_count,
            "characters": len(text),
            "chunks": len(chunks)
        })

        total_pages += page_count
        total_characters += len(text)
        total_chunks += len(chunks)

    stats = {
        "generated_at": datetime.now().isoformat(),
        "papers_directory": str(papers_dir),
        "documents_processed": len(pdf_files),
        "total_pages": total_pages,
        "total_characters": total_characters,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "total_chunks_generated": total_chunks,
        "corpus_scale": get_corpus_scale(total_chunks),
        "documents": document_stats
    }

    report_path = Path(REPORT_DIR) / "corpus_stats.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4)

    return stats


if __name__ == "__main__":
    stats = calculate_corpus_stats()

    print("\nCorpus Statistics")
    print("-----------------")
    print(f"Documents processed: {stats['documents_processed']}")
    print(f"Total pages: {stats['total_pages']}")
    print(f"Total characters: {stats['total_characters']}")
    print(f"Chunk size: {stats['chunk_size']}")
    print(f"Chunk overlap: {stats['chunk_overlap']}")
    print(f"Total chunks generated: {stats['total_chunks_generated']}")
    print(f"Corpus scale: {stats['corpus_scale']}")
    print("\nPer-document chunk counts:")

    for document in stats["documents"]:
        print(
            f"- {document['file_name']}: "
            f"{document['pages']} pages, "
            f"{document['characters']} characters, "
            f"{document['chunks']} chunks"
        )

    print("\nSaved report: reports/corpus_stats.json")