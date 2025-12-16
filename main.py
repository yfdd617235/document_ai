import os
import csv
from extract_text import extract_text_from_pdf
from invoice_parser import (
    is_invoice,
    extract_invoice_number,
    extract_invoice_date,
    extract_total,
    extract_nit,
    extract_provider,
    extract_currency
)


INPUT_FOLDER = "input_docs"
OUTPUT_FILE = "results/invoices.csv"

os.makedirs("results", exist_ok=True)

with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
    "Archivo",
    "Proveedor",
    "NIT",
    "Número factura",
    "Fecha",
    "Moneda",
    "Total"
])



    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(INPUT_FOLDER, filename)
            text = extract_text_from_pdf(path)

            if not is_invoice(text):
                continue

            writer.writerow([
    filename,
    extract_provider(text),
    extract_nit(text),
    extract_invoice_number(text),
    extract_invoice_date(text),
    extract_currency(text),
    extract_total(text)
])


print("✅ Facturas procesadas. Revisa results/invoices.csv")
