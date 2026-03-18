from app.pipeline import TextPipeline


def print_dates(title, dates):
    print(title)
    for d in dates:
        print(" ", d)


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


if __name__ == "__main__":
    pipeline = TextPipeline()

    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()

    result = pipeline.process(text)

    print("============== 检测到以下信息 =================")
    print("主语言:", result["language"])

    print_dates("日期(zh):", result["dates"]["zh"])
    print_dates("日期(es):", result["dates"]["es"])
    print_dates("日期(all):", result["dates"]["all"])

    print_countries("国家(zh):", result["countries"]["zh"])
    print_countries("国家(es):", result["countries"]["es"])
    print_countries("国家(all):", result["countries"]["all"])

    print_cities("城市(zh):", result["cities"]["zh"])
    print_cities("城市(es):", result["cities"]["es"])
    print_cities("城市(all):", result["cities"]["all"])

    print_numbers("数字(all):", result["numbers"]["all"])

    print_organizations("组织(zh):", result["organizations"]["zh"])
    print_organizations("组织(es):", result["organizations"]["es"])
    print_organizations("组织(all):", result["organizations"]["all"])

    print_persons("人物(zh):", result["persons"]["zh"])
    print_persons("人物(es):", result["persons"]["es"])
    print_persons("人物(all):", result["persons"]["all"])

    print_money("金额(all):", result["money"]["all"])