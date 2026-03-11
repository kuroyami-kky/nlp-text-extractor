import spacy
from spacy.matcher import PhraseMatcher
import re

from app.extractor.geo_extractor.entity import GEOEntity
from app.extractor.geo_extractor.patterns.city_patterns import city_zh, city_es


class CityExtractor:
    def __init__(self):
        # 分语言 tokenizer
        self.nlp_zh = spacy.blank("zh")
        self.nlp_es = spacy.blank("es")

        # 分语言 matcher
        self.matcher_zh = PhraseMatcher(self.nlp_zh.vocab, attr="NORM")
        self.matcher_es = PhraseMatcher(self.nlp_es.vocab, attr="NORM")

        patterns_zh = [self.nlp_zh(name) for name in city_zh]
        patterns_es = [self.nlp_es(name) for name in city_es]

        if patterns_zh:
            self.matcher_zh.add("CITY", patterns_zh)
        if patterns_es:
            self.matcher_es.add("CITY", patterns_es)

    def extract(self, text: str, lang: str = "auto"):

        text = self._normalize_text(text)

        if lang == "zh":
            nlp = self.nlp_zh
            matcher = self.matcher_zh
        elif lang == "es":
            nlp = self.nlp_es
            matcher = self.matcher_es

        doc = nlp(text)
        matches = matcher(doc)

        entities = []
        seen = set()

        for match_id, start, end in matches:
            span = doc[start:end]

            key = (span.start_char, span.end_char, span.text.lower())
            if key in seen:
                continue
            seen.add(key)

            entity = GEOEntity(
                text=span.text,
                start=span.start_char,
                end=span.end_char,
                label="CITY",
                source_lang=lang
            )
            entities.append(entity)

        return entities
    
    def _normalize_text(self, text: str):

        replacements = {
            "，": " ",
            "。": " ",
            "、": " ",
            "：": " ",
            "；": " ",
            "（": " ",
            "）": " "
        }

        for k, v in replacements.items():
            text = text.replace(k, v)

        return text
