from datetime import datetime, date


def clean_text(value):

    if value is None:
        return ""

    text = str(value).strip().lower()

    if text in ["unknown", "n/a", "none", "not stated"]:
        return ""

    return " ".join(text.split())


def clean_age(value):

    try:
        age = float(value)

        if age.is_integer() and 0 <= age <= 120:
            return int(age)

    except (ValueError, TypeError):
        pass

    return None


def clean_date(value):

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    if value is None:
        return None

    text = str(value).strip()

    if text.endswith(".0"):
        text = text[:-2]

    formats = [
        "%d%m%Y",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d"
    ]

    for fmt in formats:

        try:
            return datetime.strptime(text, fmt).date()

        except ValueError:
            continue

    return None

REQUIRED_COLUMNS = [
    "Case ID",
    "Age",
    "Gender",
    "Missing Location",
    "Missing Since",
    "Description"
]


def validate_columns(records):

    if not records:
        raise ValueError("The dataset is empty.")

    missing = []

    for column in REQUIRED_COLUMNS:

        if column not in records[0]:
            missing.append(column)

    if missing:
        raise ValueError(
            "Missing columns: " + ", ".join(missing)
        )

    return True


def clean_records(records):

    validate_columns(records)

    cleaned = []

    for record in records:

        item = record.copy()

        item["Age"] = clean_age(record.get("Age"))

        item["Gender"] = clean_text(
            record.get("Gender")
        )

        item["Missing Location"] = clean_text(
            record.get("Missing Location")
        )

        item["Missing Since"] = clean_date(
            record.get("Missing Since")
        )

        item["Description"] = clean_text(
            record.get("Description")
        )

        cleaned.append(item)

    return cleaned