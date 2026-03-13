class PersonEntity:

    def __init__(self, text, source_lang, start=None, end=None):
        self.text = text
        self.source_lang = source_lang
        self.start = start
        self.end = end

    def __repr__(self):
        return self.text