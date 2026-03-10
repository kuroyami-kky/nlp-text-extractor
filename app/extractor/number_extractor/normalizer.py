import re


# ---------------------------
# Chinese number conversion
# ---------------------------

ZH_DIGITS = {
    "零":0,"一":1,"二":2,"两":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,
    "壹":1,"贰":2,"叁":3,"肆":4,"伍":5,"陆":6,"柒":7,"捌":8,"玖":9
}

ZH_UNITS = {
    "十":10,"拾":10,
    "百":100,"佰":100,
    "千":1000,"仟":1000,
    "万":10000,
    "亿":100000000
}


def normalize_chinese_number(text):

    result = 0
    section = 0
    number = 0

    for char in text:

        if char in ZH_DIGITS:
            number = ZH_DIGITS[char]

        elif char in ZH_UNITS:

            unit = ZH_UNITS[char]

            if unit == 10000 or unit == 100000000:
                section = (section + number) * unit
                result += section
                section = 0
            else:
                section += number * unit

            number = 0

    return result + section + number


# ---------------------------
# Spanish number conversion
# ---------------------------

ES_UNITS = {
    "uno":1,"dos":2,"tres":3,"cuatro":4,"cinco":5,
    "seis":6,"siete":7,"ocho":8,"nueve":9,"diez":10
}

ES_TENS = {
    "once":11,"doce":12,"trece":13,"catorce":14,"quince":15,
    "veinte":20,"treinta":30,"cuarenta":40,"cincuenta":50,
    "sesenta":60,"setenta":70,"ochenta":80,"noventa":90
}

ES_HUNDREDS = {
    "cien":100,"ciento":100,
    "doscientos":200,"trescientos":300,"cuatrocientos":400,
    "quinientos":500,"seiscientos":600,"setecientos":700,
    "ochocientos":800,"novecientos":900
}

ES_SCALES = {
    "mil":1000,
    "millón":1000000,
    "millones":1000000
}


def normalize_spanish_number(text):

    tokens = text.lower().split()

    total = 0
    current = 0

    for token in tokens:

        if token in ES_UNITS:
            current += ES_UNITS[token]

        elif token in ES_TENS:
            current += ES_TENS[token]

        elif token in ES_HUNDREDS:
            current += ES_HUNDREDS[token]

        elif token in ES_SCALES:

            scale = ES_SCALES[token]

            if current == 0:
                current = 1

            current *= scale
            total += current
            current = 0

    return total + current


# ---------------------------
# Arabic number
# ---------------------------

def normalize_arabic_number(text):

    try:
        if "." in text:
            return float(text)
        return int(text)
    except:
        return None


# ---------------------------
# Main normalizer
# ---------------------------

def normalize_number(text):

    if re.fullmatch(r"\d+(\.\d+)?", text):
        return normalize_arabic_number(text)

    if re.fullmatch(r"[零一二两三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟]+", text):
        return normalize_chinese_number(text)

    if any(word in text.lower() for word in ["mil","millón","millones"]):
        return normalize_spanish_number(text)

    return None