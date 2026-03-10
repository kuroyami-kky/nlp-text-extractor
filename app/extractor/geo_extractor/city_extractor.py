import spacy
from spacy.matcher import PhraseMatcher

from app.extractor.geo_extractor.entity import GEOEntity
from app.extractor.geo_extractor.patterns.city_patterns import load_city_patterns


class CityExtractor:
    def __init__(self):
        # 分语言 tokenizer
        self.nlp_zh = spacy.blank("zh")
        self.nlp_es = spacy.blank("es")

        # 分语言 matcher
        self.matcher_zh = PhraseMatcher(self.nlp_zh.vocab, attr="LOWER")
        self.matcher_es = PhraseMatcher(self.nlp_es.vocab, attr="LOWER")

        city_names = load_city_patterns()

        patterns_zh = [self.nlp_zh.make_doc(name) for name in city_names]
        patterns_es = [self.nlp_es.make_doc(name) for name in city_names]

        self.matcher_zh.add("CITY", patterns_zh)
        self.matcher_es.add("CITY", patterns_es)

    def extract(self, text: str, lang: str = "auto"):
        if lang == "zh":
            nlp = self.nlp_zh
            matcher = self.matcher_zh
        else:
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
    
