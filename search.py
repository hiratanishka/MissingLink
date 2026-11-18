
def make_location_index(records):

    location_index = {}

    for record in records:

        location = record.get("Missing Location", "")

        if location is None:
            location = ""

        location = str(location).strip().lower()

        if location not in location_index:
            location_index[location] = []

        location_index[location].append(record)

    return location_index


def find_by_location(location_index, location):

    location = str(location).strip().lower()

    return location_index.get(location, [])


def linear_search(records, person, score_function, min_score=0):

    matches = []

    for record in records:

        score = score_function(person, record)

        if score >= min_score:
            matches.append({
                "record": record,
                "score": score
            })

    return matches
