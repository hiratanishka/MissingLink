
def get_word_score(text1, text2):

    words1 = set(str(text1 or "").lower().split())
    words2 = set(str(text2 or "").lower().split())

    if not words1 or not words2:
        return 0

    common = len(words1 & words2)
    total = len(words1 | words2)

    return common / total


def calculate_score(person1, person2):

    score = 0

    age1 = person1.get("Age")
    age2 = person2.get("Age")

    if age1 is not None and age2 is not None:

        difference = abs(age1 - age2)

        if difference == 0:
            score += 20
        elif difference <= 2:
            score += 10

    gender1 = person1.get("Gender", "")
    gender2 = person2.get("Gender", "")

    if gender1 and gender1 == gender2:
        score += 15

    location1 = person1.get("Missing Location", "")
    location2 = person2.get("Missing Location", "")

    if location1 and location1 == location2:
        score += 25

    date1 = person1.get("Missing Since")
    date2 = person2.get("Missing Since")

    if date1 is not None and date1 == date2:
        score += 15

    description1 = person1.get("Description", "")
    description2 = person2.get("Description", "")

    word_score = get_word_score(
        description1,
        description2
    )

    score += 25 * word_score

    return round(score, 2)
