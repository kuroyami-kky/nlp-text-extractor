def remove_nested_numbers(numbers):

    filtered = []

    for num in numbers:

        is_nested = False

        for other in numbers:

            if num == other:
                continue

            # check if num is inside other
            if num.start >= other.start and num.end <= other.end:

                if (other.end - other.start) > (num.end - num.start):
                    is_nested = True
                    break

        if not is_nested:
            filtered.append(num)

    return filtered