from app.pipeline import TextPipeline


def print_dates(title, dates):
    print(title)
    for d in dates:
        print(" ", d)

def print_relative_dates(title, rel_dates):
    print(title)
    for d in rel_dates:
        print(" ", d["text"], "->", d["normalized"])


def print_countries(title, countries):
    print(title)
    for c in countries:
        print(" ", c.text if hasattr(c, "text") else c)


def print_cities(title, cities):
    print(title)
    for c in cities:
        print(" ", c.text if hasattr(c, "text") else c)


def print_numbers(title, numbers):
    print(title)
    for n in numbers:
        print(" ", n.text, "->", n.value)

def print_organizations(title, organizations):
    print(title)
    for o in organizations:
        print(" ", o.text if hasattr(o, "text") else o)

def print_persons(title, persons):
    print(title)
    for p in persons:
        print(" ", p.text if hasattr(p, "text") else p)

def print_money(title, money):
    print(title)
    for m in money:
        print(" ", m.text, "->", m.normalized, m.currency)

def print_percentages(title, percentages):
    print(title)
    for p in percentages:
        text = p.get("text")
        value = p.get("value")
        subtype = p.get("subtype")
        print(" ", text, "->", value)

def print_emails(title, emails):
    print(title)
    for e in emails:
        text = e.get("text")
        value = e.get("value")
        print(" ", text)

def print_measurements(title, measurements):
    print(title)
    for m in measurements:
        text = m.get("text")
        value = m.get("value")
        unit = m.get("unit")
        standard_value = m.get("standard_value")
        standard_unit = m.get("standard_unit")
        dimension = m.get("dimension")

        if value is None:
            print(" ", text, "->", standard_unit, f"({dimension})")
        else:
            print(" ", text, "->", standard_value, standard_unit, f"({dimension})")


if __name__ == "__main__":
    pipeline = TextPipeline()

    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()

    result = pipeline.process(text)

    print("============== 检测到以下信息 =================")
    print("主语言:", result["language"])

    #print_dates("日期(zh):", result["dates"]["zh"])
    #print_dates("日期(es):", result["dates"]["es"])
    print_dates("日期(all):", result["dates"]["all"])

    #print_relative_dates("相对时间(zh):", result["relative_dates"]["zh"])
    #print_relative_dates("相对时间(es):", result["relative_dates"]["es"])
    print_relative_dates("相对时间(all):", result["relative_dates"]["all"])

    #print_countries("国家(zh):", result["countries"]["zh"])
    #print_countries("国家(es):", result["countries"]["es"])
    print_countries("国家(all):", result["countries"]["all"])

    #print_cities("城市(zh):", result["cities"]["zh"])
    #print_cities("城市(es):", result["cities"]["es"])
    print_cities("城市(all):", result["cities"]["all"])

    print_numbers("数字(all):", result["numbers"]["all"])

    #print_organizations("组织(zh):", result["organizations"]["zh"])
    #print_organizations("组织(es):", result["organizations"]["es"])
    print_organizations("组织(all):", result["organizations"]["all"])

    #print_persons("人物(zh):", result["persons"]["zh"])
    #print_persons("人物(es):", result["persons"]["es"])
    print_persons("人物(all):", result["persons"]["all"])

    print_money("金额(all):", result["money"]["all"])

    print_percentages("百分比(all):", result["percentages"]["all"])

    print_emails("邮箱(all):", result["emails"]["all"])

    print_measurements("度量衡(all):", result["measurements"]["all"])