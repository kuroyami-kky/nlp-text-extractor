from .patterns import CURRENCY_REGEX, CURRENCY_PATTERNS
from .normalizer import normalize_money
from .entity import MoneyEntity


def detect_currency(unit):
    for currency, pattern in CURRENCY_PATTERNS.items():
        import re
        if re.fullmatch(pattern, unit, re.IGNORECASE):
            return currency
    return "UNKNOWN"


def extract_money(text):
    entities = []

    for match in CURRENCY_REGEX.finditer(text):
        full_text = match.group(0)
        value_str = match.group(1)
        unit = match.group(2)

        start, end = match.span()

        value, normalized = normalize_money(value_str, unit)
        currency = detect_currency(unit)

        entity = MoneyEntity(
            text=full_text,
            value=value,
            unit=unit,
            currency=currency,
            normalized=normalized,
            start=start,
            end=end
        )

        entities.append(entity)

    return entities