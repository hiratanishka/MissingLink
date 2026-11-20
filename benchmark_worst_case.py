
from time import perf_counter

from benchmark import generate_records
from search import (
    make_location_index,
    find_by_location,
    linear_search
)
from match_score import calculate_score
from fast_results import top_matches
from merge_sort import merge_sort


def run_worst_case(size):

    records = generate_records(size)

    for record in records:
        record["Missing Location"] = "delhi"

    person = {
        "Age": 25,
        "Gender": "male",
        "Missing Location": "delhi",
        "Missing Since": None,
        "Description": "blue shirt black shoes"
    }

    start = perf_counter()

    index = make_location_index(records)
    candidates = find_by_location(index, "delhi")

    matches = linear_search(
        candidates,
        person,
        calculate_score,
        min_score=0
    )

    top_matches(matches, limit=10)

    top10_time = perf_counter() - start

    start_sort = perf_counter()
    merge_sort(matches)
    sort_time = perf_counter() - start_sort

    return {
        "Records": size,
        "Candidates": len(candidates),
        "Top10Time": top10_time,
        "MergeSortTime": sort_time
    }


if __name__ == "__main__":

    for size in [1000, 10000, 100000]:

        result = run_worst_case(size)

        print(
            result["Records"],
            result["Candidates"],
            round(result["Top10Time"], 4),
            round(result["MergeSortTime"], 4)
        )
