# app/extractor/measurement_extractor/patterns.py

import re


MASS_UNITS = {
    # kg
    "kg": {"standard_unit": "kg", "factor": 1, "dimension": "mass"},
    "kgs": {"standard_unit": "kg", "factor": 1, "dimension": "mass"},
    "kilogramo": {"standard_unit": "kg", "factor": 1, "dimension": "mass"},
    "kilogramos": {"standard_unit": "kg", "factor": 1, "dimension": "mass"},
    "kilo": {"standard_unit": "kg", "factor": 1, "dimension": "mass"},
    "kilos": {"standard_unit": "kg", "factor": 1, "dimension": "mass"},
    "公斤": {"standard_unit": "kg", "factor": 1, "dimension": "mass"},
    "千克": {"standard_unit": "kg", "factor": 1, "dimension": "mass"},

    # g
    "g": {"standard_unit": "kg", "factor": 0.001, "dimension": "mass"},
    "gr": {"standard_unit": "kg", "factor": 0.001, "dimension": "mass"},
    "gramo": {"standard_unit": "kg", "factor": 0.001, "dimension": "mass"},
    "gramos": {"standard_unit": "kg", "factor": 0.001, "dimension": "mass"},
    "克": {"standard_unit": "kg", "factor": 0.001, "dimension": "mass"},

    # t
    "t": {"standard_unit": "kg", "factor": 1000, "dimension": "mass"},
    "tonelada": {"standard_unit": "kg", "factor": 1000, "dimension": "mass"},
    "toneladas": {"standard_unit": "kg", "factor": 1000, "dimension": "mass"},
    "吨": {"standard_unit": "kg", "factor": 1000, "dimension": "mass"},
}

LENGTH_UNITS = {
    # meter
    "m": {"standard_unit": "m", "factor": 1, "dimension": "length"},
    "metro": {"standard_unit": "m", "factor": 1, "dimension": "length"},
    "metros": {"standard_unit": "m", "factor": 1, "dimension": "length"},
    "米": {"standard_unit": "m", "factor": 1, "dimension": "length"},

    # centimeter
    "cm": {"standard_unit": "m", "factor": 0.01, "dimension": "length"},
    "centímetro": {"standard_unit": "m", "factor": 0.01, "dimension": "length"},
    "centímetros": {"standard_unit": "m", "factor": 0.01, "dimension": "length"},
    "centimetro": {"standard_unit": "m", "factor": 0.01, "dimension": "length"},
    "centimetros": {"standard_unit": "m", "factor": 0.01, "dimension": "length"},
    "厘米": {"standard_unit": "m", "factor": 0.01, "dimension": "length"},

    # millimeter
    "mm": {"standard_unit": "m", "factor": 0.001, "dimension": "length"},
    "milímetro": {"standard_unit": "m", "factor": 0.001, "dimension": "length"},
    "milímetros": {"standard_unit": "m", "factor": 0.001, "dimension": "length"},
    "milimetro": {"standard_unit": "m", "factor": 0.001, "dimension": "length"},
    "milimetros": {"standard_unit": "m", "factor": 0.001, "dimension": "length"},
    "毫米": {"standard_unit": "m", "factor": 0.001, "dimension": "length"},

    # kilometer
    "km": {"standard_unit": "m", "factor": 1000, "dimension": "length"},
    "kilómetro": {"standard_unit": "m", "factor": 1000, "dimension": "length"},
    "kilómetros": {"standard_unit": "m", "factor": 1000, "dimension": "length"},
    "kilometro": {"standard_unit": "m", "factor": 1000, "dimension": "length"},
    "kilometros": {"standard_unit": "m", "factor": 1000, "dimension": "length"},
    "公里": {"standard_unit": "m", "factor": 1000, "dimension": "length"},
    "千米": {"standard_unit": "m", "factor": 1000, "dimension": "length"},
}

AREA_UNITS = {
    # square meter
    "m²": {"standard_unit": "m²", "factor": 1, "dimension": "area"},
    "m2": {"standard_unit": "m²", "factor": 1, "dimension": "area"},
    "㎡": {"standard_unit": "m²", "factor": 1, "dimension": "area"},
    "metro cuadrado": {"standard_unit": "m²", "factor": 1, "dimension": "area"},
    "metros cuadrados": {"standard_unit": "m²", "factor": 1, "dimension": "area"},
    "平方米": {"standard_unit": "m²", "factor": 1, "dimension": "area"},
    "平米": {"standard_unit": "m²", "factor": 1, "dimension": "area"},

    # square centimeter
    "cm²": {"standard_unit": "m²", "factor": 0.0001, "dimension": "area"},
    "cm2": {"standard_unit": "m²", "factor": 0.0001, "dimension": "area"},
    "centímetro cuadrado": {"standard_unit": "m²", "factor": 0.0001, "dimension": "area"},
    "centímetros cuadrados": {"standard_unit": "m²", "factor": 0.0001, "dimension": "area"},
    "centimetro cuadrado": {"standard_unit": "m²", "factor": 0.0001, "dimension": "area"},
    "centimetros cuadrados": {"standard_unit": "m²", "factor": 0.0001, "dimension": "area"},
    "平方厘米": {"standard_unit": "m²", "factor": 0.0001, "dimension": "area"},

    # square kilometer
    "km²": {"standard_unit": "m²", "factor": 1_000_000, "dimension": "area"},
    "km2": {"standard_unit": "m²", "factor": 1_000_000, "dimension": "area"},
    "kilómetro cuadrado": {"standard_unit": "m²", "factor": 1_000_000, "dimension": "area"},
    "kilómetros cuadrados": {"standard_unit": "m²", "factor": 1_000_000, "dimension": "area"},
    "kilometro cuadrado": {"standard_unit": "m²", "factor": 1_000_000, "dimension": "area"},
    "kilometros cuadrados": {"standard_unit": "m²", "factor": 1_000_000, "dimension": "area"},
    "平方公里": {"standard_unit": "m²", "factor": 1_000_000, "dimension": "area"},
    "平方千米": {"standard_unit": "m²", "factor": 1_000_000, "dimension": "area"},

    # hectare
    "ha": {"standard_unit": "m²", "factor": 10_000, "dimension": "area"},
    "hectárea": {"standard_unit": "m²", "factor": 10_000, "dimension": "area"},
    "hectáreas": {"standard_unit": "m²", "factor": 10_000, "dimension": "area"},
    "hectarea": {"standard_unit": "m²", "factor": 10_000, "dimension": "area"},
    "hectareas": {"standard_unit": "m²", "factor": 10_000, "dimension": "area"},
    "公顷": {"standard_unit": "m²", "factor": 10_000, "dimension": "area"},
}

VOLUME_UNITS = {
    # liter
    "L": {"standard_unit": "L", "factor": 1, "dimension": "volume"},
    "l": {"standard_unit": "L", "factor": 1, "dimension": "volume"},
    "lt": {"standard_unit": "L", "factor": 1, "dimension": "volume"},
    "litro": {"standard_unit": "L", "factor": 1, "dimension": "volume"},
    "litros": {"standard_unit": "L", "factor": 1, "dimension": "volume"},
    "升": {"standard_unit": "L", "factor": 1, "dimension": "volume"},

    # milliliter
    "ml": {"standard_unit": "L", "factor": 0.001, "dimension": "volume"},
    "mL": {"standard_unit": "L", "factor": 0.001, "dimension": "volume"},
    "mililitro": {"standard_unit": "L", "factor": 0.001, "dimension": "volume"},
    "mililitros": {"standard_unit": "L", "factor": 0.001, "dimension": "volume"},
    "毫升": {"standard_unit": "L", "factor": 0.001, "dimension": "volume"},

    # cubic meter
    # 第一版可以保留，但要注意它和 L 之间是 1 m³ = 1000 L
    "m³": {"standard_unit": "L", "factor": 1000, "dimension": "volume"},
    "m3": {"standard_unit": "L", "factor": 1000, "dimension": "volume"},
    "metro cúbico": {"standard_unit": "L", "factor": 1000, "dimension": "volume"},
    "metros cúbicos": {"standard_unit": "L", "factor": 1000, "dimension": "volume"},
    "metro cubico": {"standard_unit": "L", "factor": 1000, "dimension": "volume"},
    "metros cubicos": {"standard_unit": "L", "factor": 1000, "dimension": "volume"},
    "立方米": {"standard_unit": "L", "factor": 1000, "dimension": "volume"},
}

UNIT_MAP = {
    **MASS_UNITS,
    **LENGTH_UNITS,
    **AREA_UNITS,
    **VOLUME_UNITS,
}

# 单独单位抽取用：排除太短、太容易误伤的单位
UNIT_ONLY_EXCLUDE = {
    # 单字母/短符号，容易匹配到普通单词内部
    "m", "M",
    "l", "L",
    "t", "T",
    "g", "G",

    # 中文单字，容易误伤普通词
    "米",
    "克",
    "升",
    "吨",

    # 短符号，单独出现时意义不强，也容易误伤
    "kg",
    "kgs",
    "cm",
    "mm",
    "km",
    "ml",
    "mL",
    "lt",
    "ha",
}

UNIT_ONLY_MAP = {
    unit: info
    for unit, info in UNIT_MAP.items()
    if unit not in UNIT_ONLY_EXCLUDE
}

UNIT_PATTERN = "|".join(
    re.escape(unit)
    for unit in sorted(UNIT_MAP.keys(), key=len, reverse=True)
)

UNIT_ONLY_PATTERN_TEXT = "|".join(
    re.escape(unit)
    for unit in sorted(UNIT_ONLY_MAP.keys(), key=len, reverse=True)
)