from app.pipeline import TextPipeline


if __name__ == "__main__":
    pipeline = TextPipeline()

    text_zh = "2026年3月10日,中国北京有8人参会,预算壹万二千元。"
    text_es = "El 10 de marzo de 2026, en Perú, Lima, asistieron 8 delegados; el proyecto recibió un presupuesto de un millón quinientos mil soles para obras públicas y apoyo social comunitario local."

    result_zh = pipeline.process(text_zh)
    result_es = pipeline.process(text_es)

    print("============== 检测到以下信息 =================")
    print("中文:", result_zh["language"])
    print("日期:")
    for d in result_zh["dates"]:
        print(" ", d)

    print("国家:")
    for c in result_zh["countries"]:
        print(" ", c)

    print("城市:")
    for c in result_zh["cities"]:
        print(" ", c.text)

    print ("数字:")
    for c in result_zh["numbers"]:
        print(" ", c.text, "->", c.value)

    print("\n============== Se detectó lo siguiente =================")
    print("Idioma:", result_es["language"])
    print("Fechas:")
    for d in result_es["dates"]:
        print(" ", d)

    print("Países:")
    for c in result_es["countries"]:
        print(" ", c)

    print("Ciudades:")
    for c in result_es["cities"]:
        print(" ", c.text)

    print ("Numeros:")
    for c in result_es["numbers"]:
        print(" ", c.text, "->", c.value)