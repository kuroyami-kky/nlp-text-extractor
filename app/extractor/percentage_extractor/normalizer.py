# app/extractor/percentage_extractor/normalizer.py

"""
Percentage normalizer.

负责把中文 / 西语 / 阿拉伯数字形式的百分比数值统一为标准格式。

例：
15              -> 15%
15,5            -> 15.5%
十五             -> 15%
十五点五          -> 15.5%
quince          -> 15%
treinta y cinco -> 35%
"""


ZH_DIGITS = {
    "零": 0,
    "〇": 0,
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}

ZH_UNITS = {
    "十": 10,
    "百": 100,
    "千": 1000,
    "万": 10000,
    "亿": 100000000,
}


ES_NUMBERS = {
    "un": 1,
    "una": 1,
    "uno": 1,
    "dos": 2,
    "tres": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10,
    "once": 11,
    "doce": 12,
    "trece": 13,
    "catorce": 14,
    "quince": 15,
    "dieciséis": 16,
    "dieciseis": 16,
    "diecisiete": 17,
    "dieciocho": 18,
    "diecinueve": 19,
    "veinte": 20,
    "veintiuno": 21,
    "veintidós": 22,
    "veintidos": 22,
    "veintitrés": 23,
    "veintitres": 23,
    "veinticuatro": 24,
    "veinticinco": 25,
    "veintiséis": 26,
    "veintiseis": 26,
    "veintisiete": 27,
    "veintiocho": 28,
    "veintinueve": 29,
    "treinta": 30,
    "cuarenta": 40,
    "cincuenta": 50,
    "sesenta": 60,
    "setenta": 70,
    "ochenta": 80,
    "noventa": 90,
    "cien": 100,
}


def normalize_digit_number(text: str) -> float | None:
    """
    标准化阿拉伯数字。

    例：
    15   -> 15.0
    15.5 -> 15.5
    15,5 -> 15.5
    """
    if not text:
        return None

    text = text.strip()
    text = text.replace("％", "")
    text = text.replace("%", "")
    text = text.replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return None


def chinese_to_number(text: str) -> float | None:
    """
    中文数字转数字。

    支持：
    十五       -> 15
    二十       -> 20
    二十五     -> 25
    一百二十三 -> 123
    十五点五   -> 15.5
    3         -> 3
    3.5       -> 3.5
    3,5       -> 3.5
    """
    if not text:
        return None

    text = text.strip()

    # 如果本身就是阿拉伯数字
    digit_value = normalize_digit_number(text)
    if digit_value is not None:
        return digit_value

    # 处理中文小数
    if "点" in text:
        integer_part, decimal_part = text.split("点", 1)

        integer_value = chinese_to_number(integer_part)
        if integer_value is None:
            return None

        decimal_digits = []

        for char in decimal_part:
            if char in ZH_DIGITS:
                decimal_digits.append(str(ZH_DIGITS[char]))
            elif char.isdigit():
                decimal_digits.append(char)
            else:
                return None

        decimal_text = "".join(decimal_digits)

        if not decimal_text:
            return None

        return float(f"{int(integer_value)}.{decimal_text}")

    total = 0
    section = 0
    number = 0

    for char in text:
        if char in ZH_DIGITS:
            number = ZH_DIGITS[char]

        elif char in ZH_UNITS:
            unit = ZH_UNITS[char]

            if unit >= 10000:
                section = (section + number) * unit
                total += section
                section = 0
            else:
                if number == 0:
                    number = 1
                section += number * unit

            number = 0

        else:
            return None

    return float(total + section + number)


def spanish_to_number(text: str) -> float | None:
    """
    西语数字词转数字。

    支持：
    quince            -> 15
    veinte            -> 20
    veinticinco       -> 25
    treinta y cinco   -> 35
    cien              -> 100
    15                -> 15
    15,5              -> 15.5
    """
    if not text:
        return None

    text = text.lower().strip()

    digit_value = normalize_digit_number(text)
    if digit_value is not None:
        return digit_value

    if text in ES_NUMBERS:
        return float(ES_NUMBERS[text])

    # treinta y cinco / cuarenta y dos
    if " y " in text:
        parts = text.split(" y ")

        if len(parts) != 2:
            return None

        left, right = parts

        if left not in ES_NUMBERS:
            return None

        if right not in ES_NUMBERS:
            return None

        return float(ES_NUMBERS[left] + ES_NUMBERS[right])

    return None


def format_percentage(value: float | None) -> str | None:
    """
    把数字统一转成百分比字符串。

    例：
    15.0  -> 15%
    15.5  -> 15.5%
    None  -> None
    """
    if value is None:
        return None

    if value.is_integer():
        return f"{int(value)}%"

    return f"{value}%"