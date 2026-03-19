from app.extractor.date_extractor.absolute_date_extractor import DateExtractor
from app.extractor.geo_extractor.country_extractor import CountryExtractor
from app.extractor.geo_extractor.city_extractor import CityExtractor
from app.extractor.number_extractor.number_extractor import NumberExtractor
from app.extractor.organization_extractor.org_extractor import OrganizationExtractor
from app.extractor.person_extractor.person_extractor import PersonExtractor
from app.extractor.money_extractor.money_extractor import extract_money
from app.extractor.date_extractor.relative_date_extractor import extract_relative_date
from app.extractor.date_extractor.normalizer import normalize_relative_dates


import spacy

class TextPipeline:
    def __init__(self, language: str = "auto"):
        self.language = language
        
        self.nlp = spacy.load("es_core_news_md")
        self.date_extractor = DateExtractor()
        self.country_extractor = CountryExtractor()
        self.city_extractor = CityExtractor()
        self.number_extractor = NumberExtractor(self.nlp)
        self.org_extractor = OrganizationExtractor(self.nlp)
        self.person_extractor = PersonExtractor(self.nlp)

    def detect_language(self, text: str):
        # 目前只是占位逻辑
        if self.language != "auto":
            return self.language
        
        if any("\u4e00" <= char <= "\u9fff" for char in text):
            return "zh"
        return "es"
    
    def _filter_numbers_in_dates(self, numbers, dates):
        filtered = []

        for num in numbers:

            overlap = False

            for date in dates:
                if num.start >= date.start and num.end <= date.end:
                    overlap = True
                    break

            if not overlap:
                filtered.append(num)

        return filtered
    
    def _deduplicate_entities(self, entities):
        seen = set()
        unique = []

        for e in entities:
            if e.text not in seen:
                seen.add(e.text)
                unique.append(e)

        return unique
    
    def _filter_countries_in_orgs(self, countries, orgs):

        filtered = []

        for c in countries:

            overlap = False

            for o in orgs:
                if c.start >= o.start and c.end <= o.end:
                    overlap = True
                    break

            if not overlap:
                filtered.append(c)

        return filtered

    def _filter_nested_persons(self, persons):

        filtered = []

        for p in persons:

            contained = False

            for other in persons:

                if p == other:
                    continue

                if p.start >= other.start and p.end <= other.end:
                    if (other.end - other.start) > (p.end - p.start):
                        contained = True
                        break

            if not contained:
                filtered.append(p)

        return filtered

    def _filter_numbers_in_money(self, numbers, money_entities):
        money_spans = {(m.start, m.end) for m in money_entities}

        filtered = []

        for n in numbers:
            if not any(n.start >= m[0] and n.end <= m[1] for m in money_spans):
                filtered.append(n)

        return filtered
    

    def process(self, text: str):
        
        detected_lang = self.detect_language(text)

        dates_zh = self.date_extractor.extract(text, "zh")
        dates_es = self.date_extractor.extract(text, "es")
        dates = dates_zh + dates_es

        
        rel_zh_entities = extract_relative_date(text, "zh")
        rel_es_entities = extract_relative_date(text, "es")
        rel_zh = normalize_relative_dates(rel_zh_entities)
        rel_es = normalize_relative_dates(rel_es_entities)
        rel_all = rel_zh + rel_es

        countries_zh = self.country_extractor.extract(text, "zh")
        countries_zh = self._deduplicate_entities(countries_zh)
        countries_es = self.country_extractor.extract(text, "es")
        countries_es = self._deduplicate_entities(countries_es)
        countries = countries_zh + countries_es
        countries = self._deduplicate_entities(countries)
        

        cities_zh = self.city_extractor.extract(text, "zh")
        cities_zh = self._deduplicate_entities(cities_zh)
        cities_es = self.city_extractor.extract(text, "es")
        cities_es = self._deduplicate_entities(cities_es)
        cities = cities_zh + cities_es
        cities = self._deduplicate_entities(cities)

        numbers_zh = self.number_extractor.extract(text, "zh")
        numbers_zh = self._filter_numbers_in_dates(numbers_zh, dates)
        numbers_es = self.number_extractor.extract(text, "es")
        numbers_es = self._filter_numbers_in_dates(numbers_es, dates)
        numbers = numbers_zh + numbers_es
        numbers_all = self._deduplicate_entities(numbers)
        numbers_all = self._filter_numbers_in_dates(numbers_all, dates)
        
        money_entities = extract_money(text)

        numbers_all = self._filter_numbers_in_money(numbers_all, money_entities)

        organizations_zh = self.org_extractor.extract(text, "zh")
        organizations_zh = self._deduplicate_entities(organizations_zh)
        organizations_es = self.org_extractor.extract(text, "es")
        organizations_es = self._deduplicate_entities(organizations_es)
        organizations  = organizations_zh + organizations_es
        organizations = self._deduplicate_entities(organizations)
        countries = self._filter_countries_in_orgs(countries, organizations)


        persons_zh = []
        persons_es = []

        if detected_lang =="zh":
            persons_zh = self.person_extractor.extract(text, "zh")
        elif detected_lang == "es":
            persons_es = self.person_extractor.extract(text, "es")
        persons_zh = self._deduplicate_entities(persons_zh)
        persons_zh = self._filter_nested_persons(persons_zh)
        persons_es = self._deduplicate_entities(persons_es)
        persons = persons_zh + persons_es
        persons = self._deduplicate_entities(persons)

        money_entities = extract_money(text)
       


        return {
            "language": detected_lang,
            "dates": {
                "zh": dates_zh,
                "es": dates_es,
                "all": dates
            },
            "relative_dates": {
                "zh": rel_zh,
                "es": rel_es,
                "all": rel_all
            },
            "countries": {
                "zh": countries_zh,
                "es": countries_es,
                "all": countries
            },
            "cities": {
                "zh": cities_zh,
                "es": cities_es,
                "all": cities
            },
            "numbers": {
                "zh": numbers_zh,
                "es": numbers_es, 
                "all": numbers_all
            },
            "organizations": {
                "zh": organizations_zh,
                "es": organizations_es,
                "all": organizations
            },
            "persons": {
                "zh": persons_zh,
                "es": persons_es,
                "all": persons
            },
            "money":{
                "all":money_entities
            },
        }
        


