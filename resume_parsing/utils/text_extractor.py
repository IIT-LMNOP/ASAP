import pdfplumber
from docx import Document
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return clean_text(text)

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return clean_text(text)

def clean_text(text):
    # Normalize whitespace and remove control chars
    text = re.sub(r'\s+', ' ', text).strip()
    return text