import re
from app.extractor.date_extractor.patterns import (
    relative_date_patterns_zh,
    relative_date_patterns_es
)


def extract_relative_date(text: str, lang: str):
    results = []

    if lang == "zh":
        patterns = relative_date_patterns_zh
    elif lang == "es":
        patterns = relative_date_patterns_es
    else:
        return []

    for word, offset in patterns["fixed"].items():
        if word in text:
            results.append({
                "text": word,
                "offset": offset,
                "type": "relative_fixed"
            })

    for pattern in patterns["regex"]:
        matches = re.finditer(pattern, text)

        for match in matches:
            if lang == "zh":
                num = int(match.group(1))
                raw_text = match.group(0)

                if "前" in raw_text:
                    offset = -num
                else:
                    offset = num

            elif lang == "es":
                num = int(match.group(1))
                raw_text = match.group(0)

                if raw_text.startswith("hace"):
                    offset = -num
                else:
                    offset = num

            results.append({
                "text": raw_text,
                "offset": offset,
                "type": "relative_regex"
            })

    return results