# import os
# import csv
# from extract_text import extract_text_from_pdf
# from detect_dates import find_dates

# INPUT_FOLDER = "input_docs"
# OUTPUT_FILE = "results/summary.csv"

# with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Documento", "Fechas Detectadas"])

#     for filename in os.listdir(INPUT_FOLDER):
#         if filename.endswith(".pdf"):
#             path = os.path.join(INPUT_FOLDER, filename)
#             text = extract_text_from_pdf(path)
#             dates = find_dates(text)
#             writer.writerow([filename, ", ".join([str(d.date()) for d in dates])])

import os
import csv
from extract_text import extract_text_from_pdf
from analyze_text import extract_dates, detect_keywords

INPUT_FOLDER = "input_docs"
OUTPUT_FILE = "results/summary.csv"

os.makedirs("results", exist_ok=True)

with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Archivo", "Fechas encontradas", "Palabras clave"])

    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(INPUT_FOLDER, filename)

            text = extract_text_from_pdf(path)

            dates = extract_dates(text)
            keywords = detect_keywords(text)

            writer.writerow([
                filename,
                ", ".join(dates),
                ", ".join(keywords)
            ])

print("✅ Análisis completado. Revisa results/summary.csv")
