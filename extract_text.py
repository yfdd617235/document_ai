#Esto ya funciona

# import pdfplumber

# def extract_text_from_pdf(pdf_path):
#     full_text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 full_text += page_text + "\n"
#     return full_text

#-------------------------

import pdfplumber
from pdf2image import convert_from_path
import pytesseract

MIN_TEXT_LENGTH = 200  # umbral para decidir si usar OCR

def extract_text_from_pdf(pdf_path):
    full_text = ""

    # 1️⃣ Intentar lectura digital
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
    except:
        pass

    # 2️⃣ Si el texto es insuficiente → OCR
    if len(full_text.strip()) < MIN_TEXT_LENGTH:
        print(f"OCR aplicado a: {pdf_path}")
        images = convert_from_path(pdf_path)
        for img in images:
            ocr_text = pytesseract.image_to_string(img, lang="spa")
            full_text += ocr_text + "\n"

    return full_text

