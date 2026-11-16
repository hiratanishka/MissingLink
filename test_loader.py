import unittest
from io import StringIO, BytesIO
from openpyxl import Workbook

from data_loader import load_data


class TestDataLoader(unittest.TestCase):

    def test_csv_loading(self):

        sample = StringIO(
            "Case ID,Age,Gender\n"
            "TEST001,22,Male\n"
            "TEST002,25,Female"
        )

        data = load_data(sample, "sample.csv")

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["Age"], "22")

    def test_excel_loading(self):

        workbook = Workbook()
        sheet = workbook.active

        sheet.append(["Case ID", "Age"])
        sheet.append(["TEST001", 22])
        sheet.append(["TEST002", 25])

        file = BytesIO()
        workbook.save(file)
        file.seek(0)

        data = load_data(file, "sample.xlsx")

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["Age"], 22)

    def test_invalid_file(self):

        with self.assertRaises(ValueError):
            load_data(
                StringIO("Hello"),
                "sample.txt"
            )


if __name__ == "__main__":
    unittest.main()