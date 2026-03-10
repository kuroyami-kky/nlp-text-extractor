from app.extractor.date_extractor.extractor import DateExtractor
from app.extractor.geo_extractor.country_extractor import CountryExtractor
from app.extractor.geo_extractor.city_extractor import CityExtractor
from app.extractor.number_extractor.number_extractor import NumberExtractor
import spacy

class TextPipeline:
    def __init__(self, language: str = "auto"):
        self.language = language
        
        self.nlp = spacy.blank("xx")
        self.date_extractor = DateExtractor()
        self.country_extractor = CountryExtractor()
        self.city_extractor = CityExtractor()
        self.number_extractor = NumberExtractor(self.nlp)

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
    

    def process(self, text: str):
        lang = self.detect_language(text)

        dates = self.date_extractor.extract(text, lang)

        countries = self.country_extractor.extract(text, lang)
        cities = self.city_extractor.extract(text, lang)

        numbers = self.number_extractor.extract(text, lang)
        numbers = self._filter_numbers_in_dates(numbers, dates)

        return {
            "language": lang,
            "dates": dates,
            "countries": countries,
            "cities": cities,
            "numbers": numbers
        }
        


