# app/extractor/measurement_extractor/measurement_extractor.py

import re
from app.extractor.measurement_extractor.patterns import UNIT_MAP, UNIT_PATTERN, UNIT_ONLY_PATTERN_TEXT
from app.extractor.measurement_extractor.normalizer import normalize_measurement


# 第一版：只支持阿拉伯数字
# 支持：
# 150kg
# 150 kg
# 2.5 kilómetros
# 1,5 litros
# 20平方米
NUMBER_PATTERN = r"\d+(?:[.,]\d+)?"


MEASUREMENT_PATTERN = re.compile(
    rf"(?P<value>{NUMBER_PATTERN})\s*(?P<unit>{UNIT_PATTERN})",
    flags=re.IGNORECASE
)


UNIT_ONLY_PATTERN = re.compile(
    rf"(?P<unit>{UNIT_ONLY_PATTERN_TEXT})",
    flags=re.IGNORECASE
)


def parse_number(value_text: str):
    """
    将文本数字转成 float。
    第一版只处理阿拉伯数字：
    150 -> 150.0
    2.5 -> 2.5
    1,5 -> 1.5
    """
    if not value_text:
        return None

    value_text = value_text.replace(",", ".")

    try:
        return float(value_text)
    except ValueError:
        return None


def normalize_unit_key(unit_text: str):
    """
    统一 unit 的 key，主要处理西语大小写。
    中文不受影响。
    """
    if not unit_text:
        return None

    unit_text = unit_text.strip()

    if unit_text in UNIT_MAP:
        return unit_text

    lower_unit = unit_text.lower()

    if lower_unit in UNIT_MAP:
        return lower_unit

    return unit_text


def extract_measurements(text: str, include_unit_only: bool = True):
    """
    抽取文本中的度量衡表达。

    返回格式示例：
    {
        "text": "150kg",
        "start": 0,
        "end": 5,
        "value": 150.0,
        "unit": "kg",
        "standard_value": 150.0,
        "standard_unit": "kg",
        "dimension": "mass"
    }

    如果是单独单位：
    {
        "text": "平方米",
        "start": 10,
        "end": 13,
        "value": None,
        "unit": "平方米",
        "standard_value": None,
        "standard_unit": "m²",
        "dimension": "area"
    }
    """
    if not text:
        return []

    results = []
    occupied_spans = []

    # 1. 先抽取 “数字 + 单位”
    for match in MEASUREMENT_PATTERN.finditer(text):
        raw_text = match.group(0)
        value_text = match.group("value")
        unit_text = match.group("unit")

        start = match.start()
        end = match.end()

        value = parse_number(value_text)
        unit_key = normalize_unit_key(unit_text)

        normalized = normalize_measurement(value, unit_key)

        if not normalized:
            continue

        item = {
            "text": raw_text,
            "start": start,
            "end": end,
            "value": value,
            "unit": unit_text,
            "standard_value": normalized["standard_value"],
            "standard_unit": normalized["standard_unit"],
            "dimension": normalized["dimension"],
        }

        results.append(item)
        occupied_spans.append((start, end))

    # 2. 再抽取“单独单位”
    # 避免 150kg 里面的 kg 被重复抽出来
    if include_unit_only:
        for match in UNIT_ONLY_PATTERN.finditer(text):
            raw_text = match.group(0)
            unit_text = match.group("unit")

            start = match.start()
            end = match.end()

            if is_inside_existing_span(start, end, occupied_spans):
                continue

            if has_bad_latin_boundary(text, start, end):
                continue

            unit_key = normalize_unit_key(unit_text)
            normalized = normalize_measurement(None, unit_key)

            if not normalized:
                continue

            item = {
                "text": raw_text,
                "start": start,
                "end": end,
                "value": None,
                "unit": unit_text,
                "standard_value": None,
                "standard_unit": normalized["standard_unit"],
                "dimension": normalized["dimension"],
            }

            results.append(item)
            occupied_spans.append((start, end))

    return sort_and_deduplicate(results)


def is_inside_existing_span(start: int, end: int, spans: list):
    """
    判断当前 span 是否已经被更大的实体覆盖。
    例如：
    150kg 已经被抽出，那么 kg 就不再单独抽。
    """
    for span_start, span_end in spans:
        if start >= span_start and end <= span_end:
            return True

    return False


def sort_and_deduplicate(results: list):
    """
    按位置排序并去重。
    """
    results = sorted(results, key=lambda x: (x["start"], x["end"]))

    unique = []
    seen = set()

    for item in results:
        key = (item["start"], item["end"], item["text"])

        if key in seen:
            continue

        seen.add(key)
        unique.append(item)

    return unique

def is_latin_letter(char: str):
    return bool(re.match(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", char))

def has_bad_latin_boundary(text: str, start: int, end: int):
    """
    防止把单位匹配到西语单词内部。
    例如：
    calcula 里的 l
    distancia 里的 t
    """
    before = text[start - 1] if start > 0 else ""
    after = text[end] if end < len(text) else ""

    if before and is_latin_letter(before):
        return True

    if after and is_latin_letter(after):
        return True

    return False