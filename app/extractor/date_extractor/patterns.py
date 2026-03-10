import re

date_pattern_zh = [
    r"(\d{4})年(?:\s*(\d{1,2})月)?(?:\s*(\d{1,2})日)?", #样式：xxxx年xx月xx日
    r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", #样式：xxxx/xx/xx或xxxx-xx-xx或xxxx.xx.xx
    r"(\d{4})[-./](0?[1-9]|1[0-2])(?![-./])", #样式：YYYY-MM
    r"(\d{4})年\s*(\d{1,2})月" #样式：YYYY年MM月
]

date_pattern_es = [
    r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", #样式：xx/xx/xxxx或xx-xx-xxxx
    r"(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})", #样式：xx de xx de xxxx
    r"(\d{1,2})/(\d{4})", #样式：xx/xxxx
    r"(\w+)\s+de\s+(\d{4})" #样式： xx de xxxx

]