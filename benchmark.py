
from time import perf_counter
from random import Random

from search import make_location_index, find_by_location, linear_search
from match_score import calculate_score
from fast_results import top_matches
from merge_sort import merge_sort


def generate_records(size):

    rng = Random(42)

    locations = ["delhi", "noida", "mumbai", "jaipur"]

    records = []

    for i in range(size):

        records.append({
            "Case ID": f"TEST{i:06d}",
            "Age": rng.randint(18, 65),
            "Gender": rng.choice(["male", "female"]),
            "Missing Location": rng.choice(locations),
            "Missing Since": None,
            "Description": "blue shirt black shoes"
        })

    return records


def measure(function):

    start = perf_counter()
    output = function()
    duration = perf_counter() - start

    return output, duration


def benchmark(size):

    records = generate_records(size)

    person = {
        "Age": 25,
        "Gender": "male",
        "Missing Location": "delhi",
        "Missing Since": None,
        "Description": "blue shirt black shoes"
    }

    index, build_time = measure(
        lambda: make_location_index(records)
    )

    candidates, lookup_time = measure(
        lambda: find_by_location(index, "delhi")
    )

    matches, search_time = measure(
        lambda: linear_search(
            candidates,
            person,
            calculate_score,
            min_score=0
        )
    )

    _, heap_time = measure(
        lambda: top_matches(matches, limit=10)
    )

    _, sort_time = measure(
        lambda: merge_sort(matches)
    )

    total = (
        build_time + lookup_time + search_time
        + heap_time
    )

    return {
        "Records": size,
        "Candidates": len(candidates),
        "Index (s)": round(build_time, 4),
        "Lookup (s)": round(lookup_time, 4),
        "Search (s)": round(search_time, 4),
        "Heap (s)": round(heap_time, 4),
        "Merge Sort (s)": round(sort_time, 4),
        "Top 10 Total (s)": round(total, 4)
    }


if __name__ == "__main__":

    for size in [1000, 10000, 100000]:

        result = benchmark(size)

        print()
        print("Dataset:", result["Records"])
        print("Candidates:", result["Candidates"])

        for key, value in result.items():

            if key.endswith("(s)"):
                print(f"{key}: {value}")
