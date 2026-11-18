
import heapq


def top_matches(results, limit=10):

    heap = []

    for index, item in enumerate(results):

        score = item["score"]

        entry = (score, index, item)

        if len(heap) < limit:
            heapq.heappush(heap, entry)

        elif score > heap[0][0]:
            heapq.heapreplace(heap, entry)

    best = sorted(
        heap,
        key=lambda entry: entry[0],
        reverse=True
    )

    return [entry[2] for entry in best]
