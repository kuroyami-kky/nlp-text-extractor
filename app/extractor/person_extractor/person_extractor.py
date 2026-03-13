from app.nlp_engine.hanlp_pipeline import hanlp_ner
from .entity import PersonEntity
from .person_dictionary import persons_name, COMMON_SURNAMES


class PersonExtractor:

    INVALID_CHARS = set("，。！？、；：,.!?()（）《》“”\"'")
    BAD_SUFFIX = {
        "大学","公司","集团","组织","政府","医院","学院",
        "广州","北京","上海","深圳","中国","世界",
        "卫生","研究","中心","大学","医院","委员会"
        }
    BAD_SECOND_CHARS = {
        "国","广","州","市","省","大","学","组","部","局",
        "院","会","的","了","在","和","与"
        }
    BAD_LAST_CHARS = {
        "组","队","部","局","处","室","院","会","厅","科"
        }
    PERSON_CONTEXT = {
        "表示","指出","称","说","认为","介绍","强调","告诉","接受","表示"
        }
    

    def __init__(self, nlp):
        self.nlp = nlp


    # -------------------------
    # 中文姓名合法性检查
    # -------------------------
    def _valid_chinese_name(self, name):

        if len(name) not in (2,3):
            return False

        if not all('\u4e00' <= c <= '\u9fff' for c in name):
            return False

        if any(c in self.INVALID_CHARS for c in name):
            return False

        # 第二字过滤
        if name[1] in self.BAD_SECOND_CHARS:
            return False

        # 机构后缀过滤
        if name[1:] in self.BAD_SUFFIX:
            return False

        # 第三字机构字过滤
        if len(name) == 3 and name[-1] in self.BAD_LAST_CHARS:
            return False

        return True

    # -------------------------
    # 中文姓名规则
    # -------------------------
    def _rule_based_chinese_names(self, text):

        results = []

        trigger_words = ["记者", "记者：", "记者:", "本报记者"]

        for trigger in trigger_words:

            pos = text.find(trigger)

            while pos != -1:

                start = pos + len(trigger)

                name2 = text[start:start+2]
                name3 = text[start:start+3]

                if self._valid_chinese_name(name3):
                    results.append((name3, start, start+3))

                elif self._valid_chinese_name(name2):
                    results.append((name2, start, start+2))

                pos = text.find(trigger, pos + 1)

        return results

    # -------------------------
    # merge HanLP字符级结果
    # -------------------------
    def _merge_chinese_persons(self, persons):

        if not persons:
            return []

        persons = sorted(persons, key=lambda x: x.start)

        merged = []
        current = persons[0]

        for p in persons[1:]:

            if p.start == current.end:
                current.text += p.text
                current.end = p.end
            else:
                merged.append(current)
                current = p

        merged.append(current)

        return merged


    # -------------------------
    # 主函数
    # -------------------------
    def extract(self, text, source_lang):

        persons = []

        # ---------- 西语 ----------
        if source_lang == "es":

            doc = self.nlp(text)

            for ent in doc.ents:

                if ent.label_ in ["PERSON", "PER"]:

                    persons.append(
                        PersonEntity(
                            text=ent.text,
                            source_lang="es",
                            start=ent.start_char,
                            end=ent.end_char
                        )
                    )


        # ---------- 中文 ----------
        elif source_lang == "zh":

            # HanLP NER
            chars = list(text)
            result = hanlp_ner([chars])[0]

            for char, label, start, end in result:

                if label == "PERSON":

                    persons.append(
                        PersonEntity(
                            text=text[start:end],
                            source_lang="zh",
                            start=start,
                            end=end
                        )
                    )

            # merge HanLP字符级
            persons = self._merge_chinese_persons(persons)


            # ---------- 人名词典 ----------
            for name in persons_name:

                start = text.find(name)

                while start != -1:

                    persons.append(
                        PersonEntity(
                            text=name,
                            source_lang="zh",
                            start=start,
                            end=start + len(name)
                        )
                    )

                    start = text.find(name, start + 1)


            # ---------- 姓名规则 ----------
            rule_names = self._rule_based_chinese_names(text)

            for name, start, end in rule_names:

                persons.append(
                    PersonEntity(
                        text=name,
                        source_lang="zh",
                        start=start,
                        end=end
                    )
                )

        return persons