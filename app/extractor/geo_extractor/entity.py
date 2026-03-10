from dataclasses import dataclass

@dataclass
class CountryEntity:
    text: str
    source_lang: str
    start: int
    end: int

    def __repr__(self):
        return self.text
    
@dataclass    
class GEOEntity:
    def __init__(self, text: str, start: int, end: int, label: str, source_lang: str = "auto"):
        self.text = text
        self.start = start
        self.end = end
        self.label = label
        self.source_lang = source_lang

    def __repr__(self):
        return (
            f"<GEOEntity text='{self.text}' "
            f"label='{self.label}' "
            f"start={self.start} end={self.end} "
            f"source_lang='{self.source_lang}'>"
        )