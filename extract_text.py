import pdfplumber
from pdf2image import convert_from_path
import pytesseract


def extract_text_from_pdf(pdf_path):
    text = ""

    # 1️⃣ Intentar lectura digital (PDF con texto)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error leyendo PDF digital: {e}")

    # 2️⃣ Si casi no hay texto → aplicar OCR
    if len(text.strip()) < 50:
        print(f"OCR aplicado a: {pdf_path}")

        images = convert_from_path(pdf_path)
        for img in images:
            text += pytesseract.image_to_string(
                img,
                lang="spa"
            )

    return text

