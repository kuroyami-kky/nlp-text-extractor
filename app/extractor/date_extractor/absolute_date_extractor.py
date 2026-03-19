import re
from .normalizer import normalize_zh, normalize_es
from .patterns import date_pattern_zh, date_pattern_es
from .entity import DateEntity
from .deduplicate import _deduplicate



class DateExtractor:
    def __init__(self):
        pass

    def extract(self, text: str, lang: str):
        results = []


        if lang == "zh":
            patterns_zh = date_pattern_zh

            for pattern in patterns_zh:
                for match in re.finditer(pattern, text):

                    year = match.group(1)
                    month = match.group(2) if match.lastindex and match.lastindex >=2 else None 
                    day = match.group(3) if match.lastindex and match.lastindex >= 3 else None
                    
                    y, mm, dd = normalize_zh(year, month, day)

                    results.append(
                        DateEntity(
                            text=match.group(0),
                            start=match.start(),
                            end=match.end(),
                            year=y,
                            month=mm,
                            day=dd,
                            source_lang="zh"
                        )
                    )

                


        if lang == "es":
            patterns_es = date_pattern_es

            for pattern in patterns_es:
                for match in re.finditer(pattern, text):

                    if match.lastindex == 3:
                        # 3 个 group：一定有 day
                        day = match.group(1)
                        month = match.group(2)
                        year = match.group(3)

                        normalized_es = normalize_es(year, month, day)

                    elif match.lastindex == 2:
                        # 2 个 group：只有 year + month
                        g1 = match.group(1)
                        g2 = match.group(2)

                        if g1.isdigit():
                            # 02/2026 这种
                            month = g1
                            year = g2
                        else:
                            # mayo de 2026 这种
                            month = g1
                            year = g2

                    y, mm, dd = normalize_es(year, month, day)

                    results.append(
                        DateEntity(
                            text=match.group(0),
                            start=match.start(),
                            end=match.end(),
                            year=y,
                            month=mm,
                            day=dd,
                            source_lang="es"
                        )
                    )
        
        results = _deduplicate(results)
        return results

    


