# app/extractor/percentage_extractor/patterns.py

# 阿拉伯数字：
# 15
# 15.5
# 15,5
# +15
# -15
DIGIT_NUMBER = r"""
[+-]?
\d+
(?:[.,]\d+)?
"""


# 中文数字：
# 十五
# 二十
# 二十五
# 一百二十三
# 十五点五
# 三点二
# 15
# 15.5
ZH_NUMBER = r"""
(?:\d+(?:[.,]\d+)?)
|
(?:[零〇一二两三四五六七八九十百千万亿]+(?:点[零〇一二两三四五六七八九\d]+)?)
"""


# 西语数字词：
# un
# cinco
# quince
# veinte
# veinticinco
# treinta y cinco
# cien
ES_NUMBER_WORD = r"""
(?:
    un|una|uno|
    dos|tres|cuatro|cinco|seis|siete|ocho|nueve|
    diez|once|doce|trece|catorce|quince|
    dieciséis|dieciseis|diecisiete|dieciocho|diecinueve|
    veinte|veintiuno|veintidós|veintidos|veintitrés|veintitres|
    veinticuatro|veinticinco|veintiséis|veintiseis|
    veintisiete|veintiocho|veintinueve|
    treinta|cuarenta|cincuenta|sesenta|setenta|ochenta|noventa|
    cien
)
(?:\s+y\s+
    (?:
        un|una|uno|
        dos|tres|cuatro|cinco|seis|siete|ocho|nueve
    )
)?
"""


# 1. 15%, 15.5%, 15,5%, 15 ％
PERCENT_SYMBOL_PATTERN = rf"""
(?P<number>{DIGIT_NUMBER})
\s*
[%％]
"""


# 2. 百分之十五、百分之15、百分之十五点五
ZH_PERCENT_PATTERN = rf"""
百分之
(?P<zh_number>{ZH_NUMBER})
"""


# 3. 15 por ciento, 15,5 por ciento, 15 porcentaje
ES_PERCENT_DIGIT_PATTERN = rf"""
(?P<number>{DIGIT_NUMBER})
\s*
(?:por\s+ciento|porcentaje)
"""


# 4. quince por ciento, treinta y cinco por ciento
ES_PERCENT_WORD_PATTERN = rf"""
(?P<es_number>{ES_NUMBER_WORD})
\s+
por\s+ciento
"""


# 5A. 15个百分点、15.5个百分点
ZH_PERCENTAGE_POINT_PATTERN = rf"""
(?P<number>{DIGIT_NUMBER})
\s*
个百分点
"""


# 5B. 15 puntos porcentuales, 1 punto porcentual
ES_PERCENTAGE_POINT_PATTERN = rf"""
(?P<number>{DIGIT_NUMBER})
\s*
puntos?
\s+
porcentuales?
"""