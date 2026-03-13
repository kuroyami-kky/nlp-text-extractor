import spacy
import hanlp

print("Testing spaCy...")

nlp = spacy.load("es_core_news_md")
doc = nlp("Pedro Sánchez se reunió con Elon Musk en Madrid.")

for ent in doc.ents:
    print(ent.text, ent.label_)

print("\nTesting HanLP...")

ner = hanlp.load(hanlp.pretrained.ner.MSRA_NER_ELECTRA_SMALL_ZH)

text = "习近平在北京会见了马云"
result = ner([list(text)])

print(result)