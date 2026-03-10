import csv
from pathlib import Path
from app.extractor.geo_extractor.patterns.country_patterns import countries_es, countries_zh


def load_city_patterns():
    """
    从 cities_multilingual.csv 读取城市名称和别名，
    返回一个去重后的城市名称列表。
    """
    csv_path = Path(__file__).parent / "cities_multilingual.csv"

    city_names = []
    seen = set()

    # 读取国家名称，做冲突过滤
    country_names = set()
    for name in countries_zh:
        country_names.add(name.lower())

    for name in countries_es:
        country_names.add(name.lower())

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # 1. 主名称
            name = row["name"].strip()
            if name:
                key = name.lower()
                if key not in seen and key not in country_names:
                    city_names.append(name)
                    seen.add(key)

            # 2. 别名
            aliases = row["aliases"].strip()
            if aliases:
                for alias in aliases.split("|"):
                    alias = alias.strip()
                    if not alias:
                        continue

                    key = alias.lower()
                    if key not in seen and key not in country_names:
                        city_names.append(alias)
                        seen.add(key)

    return city_names