
from match_score import calculate_score
from check_differences import check_differences


def find_case_links(person, records, min_score=55):

    links = []

    person_location = str(
        person.get("Missing Location") or ""
    ).strip().lower()

    if not person_location:
        return links

    for record in records:

        record_location = str(
            record.get("Missing Location") or ""
        ).strip().lower()

        if not record_location:
            continue

        if record_location == person_location:
            continue

        if (
            person.get("Case ID")
            and person.get("Case ID") == record.get("Case ID")
        ):
            continue

        score = calculate_score(person, record)

        warnings = check_differences(person, record)

        if score >= min_score and not warnings:

            links.append({
                "record": record,
                "score": score
            })

    links.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return links
