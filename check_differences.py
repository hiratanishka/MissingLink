
def check_differences(person1, person2):

    warnings = []

    age1 = person1.get("Age")
    age2 = person2.get("Age")

    if age1 is not None and age2 is not None:
        if abs(age1 - age2) > 10:
            warnings.append("Large age difference")

    gender1 = str(person1.get("Gender") or "").strip().lower()
    gender2 = str(person2.get("Gender") or "").strip().lower()

    if gender1 and gender2 and gender1 != gender2:
        warnings.append("Different gender")

    return warnings
