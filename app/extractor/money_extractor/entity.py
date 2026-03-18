class MoneyEntity:
    def __init__(self, text, value, unit, currency, normalized, start, end):
        self.text = text
        self.value = value
        self.unit = unit
        self.currency = currency
        self.normalized = normalized
        self.start = start
        self.end = end

    def __repr__(self):
        return f"{self.text} -> {self.normalized} {self.currency}"