import re
from .patterns import org_zh, org_es
from .entity import OrganizationEntity

class OrganizationExtractor: 
    def __init__(self,nlp):
        self.nlp=nlp
        print("OrganizationExtractor loaded")

    def _remove_nested_entities(self, entities):

        entities = sorted(entities, key=lambda x: (x.start, -(x.end-x.start)))

        filtered = []

        for e in entities:

            overlap = False

            for f in filtered:
                if e.start >= f.start and e.end <= f.end:
                    overlap = True
                    break

            if not overlap:
                filtered.append(e)

        return filtered

    def extract(self, text:str, lang:str):
        results=[]

        if lang == "zh":
            organizations_patterns_zh = sorted(org_zh, key=len, reverse=True)

            for pattern in organizations_patterns_zh:
                for match in re.finditer(pattern, text):

                    results.append(
                        OrganizationEntity(
                            text = match.group(),
                            source_lang="zh",
                            start=match.start(),
                            end=match.end()
                        )
                    )

        elif lang == "es":
            organizations_patterns_es= sorted(org_es, key=len, reverse=True)

            for pattern in organizations_patterns_es:
                for match in re.finditer(pattern, text):

                    results.append(
                        OrganizationEntity(
                           text = match.group(),
                            source_lang="es",
                            start=match.start(),
                            end=match.end() 
                        )
                    )
        results = self._remove_nested_entities(results)
        return results