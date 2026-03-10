from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DateEntity:
    text: str
    start: int
    end: int

    year: int
    month: Optional[int]
    day: Optional[int]

    source_lang: str

    @property
    def precision(self) -> int:
        if self.day is not None:
            return 3
        if self.month is not None:
            return 2
        return 1

    @property
    def normalized(self) -> str:
        if self.day is not None:
            return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"
        if self.month is not None:
            return f"{self.year:04d}-{self.month:02d}"
        return f"{self.year:04d}"

    def __repr__(self):
        return f" {self.text} -> {self.normalized}"
