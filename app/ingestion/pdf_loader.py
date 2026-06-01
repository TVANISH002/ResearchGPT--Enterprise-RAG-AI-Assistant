from pathlib import Path
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a single PDF file.
    """
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def load_pdfs(folder_path: str) -> dict:
    """
    Load all PDFs from a folder.

    Returns:
        {
            "paper_name.pdf": "extracted text..."
        }
    """
    folder = Path(folder_path)
    pdf_texts = {}

    for pdf_file in sorted(folder.glob("*.pdf")):
        pdf_texts[pdf_file.name] = extract_text_from_pdf(str(pdf_file))

    return pdf_texts


def count_pdf_pages(pdf_path: str) -> int:
    """
    Count pages in a PDF.
    """
    reader = PdfReader(pdf_path)
    return len(reader.pages)