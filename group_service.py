
from groups import make_groups
from match_score import calculate_score
from check_differences import check_differences
from search import make_location_index


def find_possible_groups(records, min_score=70):

    index = make_location_index(records)

    positions = {
        id(record): i
        for i, record in enumerate(records)
    }

    pairs = []

    for location, candidates in index.items():

        if not location:
            continue

        for i in range(len(candidates)):

            for j in range(i + 1, len(candidates)):

                person1 = candidates[i]
                person2 = candidates[j]

                score = calculate_score(
                    person1,
                    person2
                )

                warnings = check_differences(
                    person1,
                    person2
                )

                if score >= min_score and not warnings:

                    pairs.append((
                        positions[id(person1)],
                        positions[id(person2)]
                    ))

    groups = make_groups(len(records), pairs)

    return [
        [records[index] for index in group]
        for group in groups
        if len(group) > 1
    ]
