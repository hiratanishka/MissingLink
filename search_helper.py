
def suggest_next_detail(person, records):

    if not records:
        return "Load records to start searching."

    fields = [
        ("Description", "Add a description"),
        ("Missing Location", "Add the missing location"),
        ("Age", "Add the person's age"),
        ("Missing Since", "Add the missing date"),
        ("Gender", "Add the gender if known")
    ]

    for field, message in fields:

        value = person.get(field)

        if value is None or str(value).strip() == "":
            return message + " to improve the search."

    return "All main details are provided."
