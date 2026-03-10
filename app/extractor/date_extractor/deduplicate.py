def _deduplicate(items):
        # 先按 start 升序，end 降序
        items = sorted(items, key=lambda x: (x.start, -x.end))

        unique = []

        for item in items:
            keep = True

            for u in unique:
                # 是否有重叠
                if not (item.end <= u.start or item.start >= u.end):

                    # 如果精度更高，替换
                    if item.precision > u.precision:
                        unique.remove(u)
                        unique.append(item)

                    keep = False
                    break

            if keep:
                unique.append(item)

        return unique
