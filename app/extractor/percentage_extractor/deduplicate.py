def remove_percentage_overlaps(results: list[dict]) -> list[dict]:
    """
    只处理百分比模块内部的重叠结果。

    规则：
    1. start 更靠前的优先
    2. 如果 start 相同，span 更长的优先
    3. 遇到重叠结果，保留已经选中的结果
    """
    if not results:
        return []

    sorted_results = sorted(
        results,
        key=lambda x: (x["start"], -(x["end"] - x["start"]))
    )

    filtered = []

    for item in sorted_results:
        has_overlap = False

        for kept in filtered:
            if spans_overlap(item, kept):
                has_overlap = True
                break

        if not has_overlap:
            filtered.append(item)

    return filtered


def spans_overlap(a: dict, b: dict) -> bool:
    return not (a["end"] <= b["start"] or a["start"] >= b["end"])