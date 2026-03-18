import re

CURRENCY_PATTERNS = {
    "CNY": r"(元|块|人民币|万元|千元)",
    "PEN": r"(sol|soles)",
    "USD": r"(dólar|dólares|USD|\$)",
    "EUR": r"(euro|euros|€)",
}

CURRENCY_REGEX = re.compile(
    rf"(\d+(?:[.,]\d+)?)\s?({'|'.join(v for v in CURRENCY_PATTERNS.values())})",
    re.IGNORECASE
)

MULTIPLIERS = {
    "万元": 10000,
    "千元": 1000,
    "元": 1,
    "块": 1,
}