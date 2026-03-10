class NumberEntity:

    def __init__(self, text, value, start, end):

        self.text = text
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self):

        return f"<NumberEntity text='{self.text}' value={self.value}>"