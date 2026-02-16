import pdfplumber
from docx import Document
import os

def parse_resume(file_path: str) -> dict:
    """
    Extract raw text from a resume file and return structured data.
    Supports PDF and DOCX.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Resume not found: {file_path}")

    text = ""

    if file_path.lower().endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    elif file_path.lower().endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    else:
        raise ValueError("Unsupported resume format. Use PDF or DOCX.")

    return {
        "raw_text": text.strip()
    }
