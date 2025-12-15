import re

DATE_PATTERN = r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"

def extract_dates(text):
    return list(set(re.findall(DATE_PATTERN, text)))

def detect_keywords(text):
    keywords = [
        "vencimiento",
        "plazo",
        "fecha límite",
        "caducidad",
        "expira",
        "obligación",
        "SLT",
    ]

    found = []
    text_lower = text.lower()

    for k in keywords:
        if k in text_lower:
            found.append(k)

    return found
