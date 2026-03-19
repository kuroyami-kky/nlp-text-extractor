from datetime import datetime, timedelta

def normalize_zh(year: str, month: str | None, day: str | None):
    y = int(year)
    m = int(month) if month else None
    d = int(day) if day else None
    return y, m, d


MONTH_MAP = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}

def normalize_es(year: str, month: str | None, day: str | None):
    if month and not month.isdigit():
        month = MONTH_MAP.get(month.lower())

    y = int(year)
    m = int(month) if month else None
    d = int(day) if day else None

    return y, m, d


def normalize_relative_dates(entities):
    today = datetime.today()
    results = []

    for ent in entities:
        offset = ent["offset"]
        norm_date = (today + timedelta(days=offset)).strftime("%Y-%m-%d")

        results.append({
            "text": ent["text"],
            "normalized": norm_date
        })

    return results