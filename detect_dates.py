import re
from dateutil import parser

def find_dates(text):
    date_patterns = [
        r"\d{1,2}/\d{1,2}/\d{2,4}",
        r"\d{1,2}-\d{1,2}-\d{2,4}",
        r"\d{1,2} de [a-zA-Z]+ de \d{4}"
    ]

    found_dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            try:
                found_dates.append(parser.parse(m, dayfirst=True))
            except:
                pass
    return list(set(found_dates))
