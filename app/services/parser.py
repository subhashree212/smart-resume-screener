import PyPDF2
import io

def parse_pdf(file_bytes):
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text.strip()

def parse_text(text):
    return text.strip()
