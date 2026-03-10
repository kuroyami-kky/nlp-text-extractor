from app.extractor.date_extractor.extractor import DateExtractor
from app.extractor.geo_extractor.country_extractor import CountryExtractor
from app.extractor.geo_extractor.city_extractor import CityExtractor

class TextPipeline:
    def __init__(self, language: str = "auto"):
        self.language = language
        self.date_extractor = DateExtractor()
        self.country_extractor = CountryExtractor()
        self.city_extractor = CityExtractor()

    def detect_language(self, text: str):
        # 目前只是占位逻辑
        if self.language != "auto":
            return self.language
        
        if any("\u4e00" <= char <= "\u9fff" for char in text):
            return "zh"
        return "es"

    def process(self, text: str):
        lang = self.detect_language(text)

        dates = self.date_extractor.extract(text, lang)

        countries = self.country_extractor.extract(text, lang)
        cities = self.city_extractor.extract(text, lang)

        return {
            "language": lang,
            "dates": dates,
            "countries": countries,
            "cities": cities
        }
        


