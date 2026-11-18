
def merge_sort(results):

    if len(results) <= 1:
        return results[:]

    middle = len(results) // 2

    left = merge_sort(results[:middle])
    right = merge_sort(results[middle:])

    return merge(left, right)


def merge(left, right):

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i]["score"] >= right[j]["score"]:
            result.append(left[i])
            i += 1

        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result
