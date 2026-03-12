from dataclasses import dataclass

@dataclass
class OrganizationEntity:
    text: str
    source_lang: str
    start: int
    end: int

    def __repr__(self):
        return self.text