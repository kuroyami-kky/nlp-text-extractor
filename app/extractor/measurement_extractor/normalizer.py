# app/extractor/measurement_extractor/normalizer.py

from app.extractor.measurement_extractor.patterns import UNIT_MAP


def normalize_measurement(value, unit):
    if not unit:
        return None

    unit_info = UNIT_MAP.get(unit)

    if not unit_info:
        return None

    standard_unit = unit_info["standard_unit"]
    factor = unit_info["factor"]
    dimension = unit_info["dimension"]

    if value is None:
        standard_value = None
    else:
        standard_value = value * factor

    return {
        "standard_value": standard_value,
        "standard_unit": standard_unit,
        "dimension": dimension,
    }