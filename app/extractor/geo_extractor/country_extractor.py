import re
from .patterns.country_patterns import countries_zh, countries_es
from .entity import CountryEntity

class CountryExtractor:
    def __init__(self):  
        pass

    def extract(self, text:str, lang:str):
        results=[]

        if lang == "zh":
            countries_patterns_zh = sorted(countries_zh, key=len, reverse=True)

            for pattern in countries_patterns_zh:
                for match in re.finditer(pattern, text):

                    results.append(
                        CountryEntity(
                            text = match.group(),
                            source_lang="zh",
                            start=match.start(),
                            end=match.end()
                        )
                    )

        if lang == "es":
            countries_patterns_es = sorted(countries_es, key=len, reverse=True)

            for pattern in countries_patterns_es:
                for match in re.finditer(pattern, text):

                    results.append(
                        CountryEntity(
                            text = match.group(),
                            source_lang="es",
                            start=match.start(),
                            end=match.end()
                        )
                    )
        return results