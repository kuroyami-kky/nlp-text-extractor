from app.pipeline import TextPipeline


if __name__ == "__main__":
    pipeline = TextPipeline()

    text_zh = "2024年5月我在中国北京写信，6/1飞往法国巴黎，再计划去日本东京旅游时间2025-10-01回沪。"
    text_es = "El 3 de mayo de 2024 escribí en Lima, Perú. El 06/01/2024 viajé a Madrid, España, y luego a París, Francia. Planeo visitar Tokio, Japón, el 10-10-2025. También recuerdo que el 1 de julio de 2023 estuve en Bogotá, Colombia."

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
