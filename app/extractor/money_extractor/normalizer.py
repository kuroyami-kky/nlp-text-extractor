from .patterns import MULTIPLIERS

def normalize_money(value_str, unit):
    # 处理小数/逗号
    value_str = value_str.replace(",", ".")
    value = float(value_str)

    multiplier = 1

    for k, v in MULTIPLIERS.items():
        if k in unit:
            multiplier = v
            break

    normalized = value * multiplier

    return value, normalized