# app/extractor/percentage_extractor/percentage_extractor.py

import re

from app.extractor.percentage_extractor.patterns import (
    PERCENT_SYMBOL_PATTERN,
    ZH_PERCENT_PATTERN,
    ES_PERCENT_DIGIT_PATTERN,
    ES_PERCENT_WORD_PATTERN,
    ZH_PERCENTAGE_POINT_PATTERN,
    ES_PERCENTAGE_POINT_PATTERN,
)

from app.extractor.percentage_extractor.normalizer import (
    normalize_digit_number,
    chinese_to_number,
    spanish_to_number,
    format_percentage,
)

from app.extractor.percentage_extractor.deduplicate import (
    remove_percentage_overlaps,
)


class PercentageExtractor:
    def __init__(self):
        self.pattern_configs = [
            {
                "name": "zh_percentage_point",
                "pattern": ZH_PERCENTAGE_POINT_PATTERN,
                "number_group": "number",
                "normalizer": normalize_digit_number,
                "subtype": "percentage_point",
            },
            {
                "name": "es_percentage_point",
                "pattern": ES_PERCENTAGE_POINT_PATTERN,
                "number_group": "number",
                "normalizer": normalize_digit_number,
                "subtype": "percentage_point",
            },
            {
                "name": "percent_symbol",
                "pattern": PERCENT_SYMBOL_PATTERN,
                "number_group": "number",
                "normalizer": normalize_digit_number,
                "subtype": "percentage",
            },
            {
                "name": "zh_percent",
                "pattern": ZH_PERCENT_PATTERN,
                "number_group": "zh_number",
                "normalizer": chinese_to_number,
                "subtype": "percentage",
            },
            {
                "name": "es_percent_digit",
                "pattern": ES_PERCENT_DIGIT_PATTERN,
                "number_group": "number",
                "normalizer": normalize_digit_number,
                "subtype": "percentage",
            },
            {
                "name": "es_percent_word",
                "pattern": ES_PERCENT_WORD_PATTERN,
                "number_group": "es_number",
                "normalizer": spanish_to_number,
                "subtype": "percentage",
            },
        ]

    def extract(self, text: str) -> list[dict]:
        if not text:
            return []

        results = []

        for config in self.pattern_configs:
            regex = re.compile(config["pattern"], re.IGNORECASE | re.VERBOSE)

            for match in regex.finditer(text):
                number_text = match.group(config["number_group"])
                value = config["normalizer"](number_text)
                normalized = format_percentage(value)

                if normalized is None:
                    continue

                results.append({
                    "text": match.group(0),
                    "type": "Percentage",
                    "value": normalized,
                    "subtype": config["subtype"],
                    "start": match.start(),
                    "end": match.end(),
                })

        return remove_percentage_overlaps(results)


def extract_percentage(text: str) -> list[dict]:
    return PercentageExtractor().extract(text)