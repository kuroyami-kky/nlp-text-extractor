import re

number_pattern_arabic = [
    r"\d+(\.\d+)?"
]


number_pattern_zh_regex = [
    r"[零一二两三四五六七八九壹贰叁肆伍陆柒捌玖][零一二两三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟]*"
]



number_pattern_es_large_regex = [

    # un millón / dos millones
    r"(?:un|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)\s+mill[oó]n(?:es)?",

    # quinientos mil / doscientos mil
    r"\b\w+\s+mil\b",

    # un millón quinientos mil
    r"(?:un|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)\s+mill[oó]n(?:es)?\s+\w+\s+mil"
]
