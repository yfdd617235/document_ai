import re
from collections import Counter

# ---------- DETECCIÓN DE FACTURA ----------
def is_invoice(text):
    keywords = [
        "factura", "invoice",
        "factura de venta",
        "electronic invoice",
        "invoice number"
    ]
    t = text.lower()
    return any(k in t for k in keywords)


# ---------- NÚMERO DE FACTURA ----------
def extract_invoice_number(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    text_lower = text.lower()

    # ===== PRIORIDAD 1: Etiquetas fuertes =====
    strong_labels = [
        "invoice number",
        "invoice no",
        "invoice #",
        "factura no",
        "factura nro",
        "factura número",
        "no."
    ]

    for i, line in enumerate(lines):
        for label in strong_labels:
            if label in line.lower():
                # Caso: INVOICE NUMBER 221383833
                match = re.search(r"([A-Z]{0,3}\d{5,})", line)
                if match:
                    return match.group(1)

                # Caso: número en línea siguiente
                if i + 1 < len(lines):
                    candidate = lines[i + 1]
                    if re.match(r"[A-Z]{0,3}\d{5,}", candidate):
                        return candidate

    # ===== PRIORIDAD 2: Números repetidos (Jeppesen style) =====
    candidates = []
    for line in lines:
        match = re.fullmatch(r"[A-Z]{0,3}\d{6,}", line)
        if match:
            candidates.append(match.group())

    if candidates:
        most_common = Counter(candidates).most_common(1)[0][0]
        return most_common

    # ===== PRIORIDAD 3: FEE / Prefijos DIAN =====
    match = re.search(r"\b(FEE\d{3,}|[A-Z]{1,3}\d{4,})\b", text)
    if match:
        return match.group(1)

    return ""


# ---------- FECHA ----------
def extract_invoice_date(text):
    patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b\d{1,2}-[A-Z]{3}-\d{2}\b"  # 17-OCT-21
    ]

    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return ""


# ---------- TOTAL ----------
def extract_total(text):
    patterns = [
        r"total\s*a\s*pagar\s*\$?\s*([\d\.,]+)",
        r"amount\s*due.*?\$?\s*([\d\.,]+)",
        r"please pay.*?\$?\s*([\d\.,]+)",
        r"subtotal\s*\$?\s*([\d\.,]+)"
    ]

    import re
    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            return match.group(1)

    return ""




# ---------- NIT / TAX ID ----------
def extract_nit(text):
    patterns = [
        r"nit\s*[:\-]?\s*([\d\.\-]+)",
        r"ein\s*[:\-]?\s*([\d\-]+)",
        r"tax id\s*[:\-]?\s*([\d\-]+)"
    ]

    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return ""


# ---------- PROVEEDOR ----------
def extract_provider(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    blacklist = [
        "invoice", "factura", "bill to", "ship to",
        "page", "account", "tel", "fax"
    ]

    for line in lines[:20]:  # solo primeras líneas
        if (
            len(line) > 5
            and not any(b in line.lower() for b in blacklist)
            and not line.isdigit()
        ):
            return line

    return ""

#-------------------Moneda--------------------------------
def extract_currency(text):
    text_upper = text.upper()

    if "USD" in text_upper:
        return "USD"
    if "COP" in text_upper:
        return "COP"
    if "$" in text_upper:
        return "COP"  # en Colombia casi siempre $

    return ""



# ---------- DESCRIPCIÓN / CONCEPTO ----------
def extract_description(text):
    lines = text.splitlines()
    capture = False
    desc = []

    for line in lines:
        l = line.strip()

        if any(k in l.lower() for k in ["description", "item", "service"]):
            capture = True
            continue

        if capture:
            if any(k in l.lower() for k in ["subtotal", "total", "tax"]):
                break
            if len(l) > 10:
                desc.append(l)

    return " | ".join(desc[:5])

