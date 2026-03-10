import re

from .patterns import (
    number_pattern_arabic,
    number_pattern_zh_regex,
    number_pattern_es_large_regex
)

from app.extractor.number_extractor.entity import NumberEntity
from .deduplicate import remove_nested_numbers
from .normalizer import normalize_number


class NumberExtractor:

    def __init__(self, nlp):

        self.nlp = nlp

        # add chinese patterns        
        self.regex_patterns = []

        for p in number_pattern_arabic:
            self.regex_patterns.append(re.compile(p))

        for p in number_pattern_zh_regex:
            self.regex_patterns.append(re.compile(p))

        # add spanish patterns
        for p in number_pattern_es_large_regex:
            self.regex_patterns.append(re.compile(p, re.IGNORECASE))


       



    def extract(self, text, lang):

        doc = self.nlp(text)

        results = []

        for pattern in self.regex_patterns:

            for match in pattern.finditer(text):

                value = normalize_number(match.group())

                entity = NumberEntity(
                    text=match.group(),
                    value=value,
                    start=match.start(),
                    end=match.end()
                )

                results.append(entity)

        results = remove_nested_numbers(results)

        return results
        
    