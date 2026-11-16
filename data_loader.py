import csv
from io import StringIO
from openpyxl import load_workbook


def load_data(file, file_name):

    file_name = file_name.lower()

    if file_name.endswith(".csv"):

        content = file.read()

        if isinstance(content, bytes):
            content = content.decode("utf-8-sig")

        records = list(
            csv.DictReader(StringIO(content))
        )

        return records

    elif file_name.endswith(".xlsx"):

        workbook = load_workbook(
            file,
            read_only=True,
            data_only=True
        )

        try:
            if "Missing Notices" in workbook.sheetnames:
                sheet = workbook["Missing Notices"]
            else:
                sheet = workbook.active

            rows = sheet.iter_rows(values_only=True)

            headers = next(rows, None)

            if headers is None:
                return []

            records = []

            for row in rows:
                if any(value is not None for value in row):
                    record = dict(zip(headers, row))
                    records.append(record)

            return records

        finally:
            workbook.close()

    else:
        raise ValueError(
            "Please use an Excel or CSV file."
        )