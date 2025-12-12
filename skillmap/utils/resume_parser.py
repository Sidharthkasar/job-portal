import PyPDF2
from docx import Document

def extract_text_from_resume(file):
    """
    Extract text from PDF or DOCX resume files.
    """
    text = ""
    if file.name.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    elif file.name.endswith('.docx'):
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        text = file.read().decode('utf-8')
    return text
