import unittest

from src.transform import clean_data


class TestCleanData(unittest.TestCase):

    def test_removes_extra_spaces_and_fixes_capitalization(self):
        rows = [
            {
                "id": "1",
                "date": "2026-01-05",
                "municipality": " johannesburg ",
                "service": " WATER ",
                "area": " soweto ",
                "status": " resolved "
            }
        ]

        result, _ = clean_data(rows)

        self.assertEqual(result[0]["municipality"], "Johannesburg")
        self.assertEqual(result[0]["service"], "Water")
        self.assertEqual(result[0]["area"], "Soweto")
        self.assertEqual(result[0]["status"], "Resolved")

    def test_removes_rows_with_missing_municipality(self):
        rows = [
            {
                "id": "1",
                "date": "2026-01-05",
                "municipality": "",
                "service": "Water",
                "area": "Soweto",
                "status": "Resolved"
            }
        ]

        result, _ = clean_data(rows)

        self.assertEqual(len(result), 0)

    def test_removes_duplicate_ids(self):
        rows = [
            {
                "id": "1",
                "date": "2026-01-05",
                "municipality": "Johannesburg",
                "service": "Water",
                "area": "Soweto",
                "status": "Resolved"
            },
            {
                "id": "1",
                "date": "2026-01-05",
                "municipality": "Johannesburg",
                "service": "Water",
                "area": "Soweto",
                "status": "Resolved"
            }
        ]

        result, _ = clean_data(rows)

        self.assertEqual(len(result), 1)

    def test_keeps_valid_record(self):
        rows = [
            {
                "id": "1",
                "date": "2026-01-05",
                "municipality": "Johannesburg",
                "service": "Water",
                "area": "Soweto",
                "status": "Resolved"
            }
        ]

        result, _ = clean_data(rows)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "1")

    def test_reports_rejected_records(self):
        rows = [
            {
                "id": "1",
                "date": "2026-01-05",
                "municipality": "",
                "service": "Water",
                "area": "Soweto",
                "status": "Resolved"
            },
            {
                "id": "2",
                "date": "2026-01-06",
                "municipality": "Johannesburg",
                "service": "Water",
                "area": "Soweto",
                "status": "Resolved"
            },
            {
                "id": "2",
                "date": "2026-01-06",
                "municipality": "Johannesburg",
                "service": "Water",
                "area": "Soweto",
                "status": "Resolved"
            }
        ]

        result, quality_report = clean_data(rows)

        self.assertEqual(len(result), 1)
        self.assertEqual(quality_report["duplicate_records"], 1)
        self.assertEqual(quality_report["missing_fields"], 1)
        self.assertEqual(len(quality_report["rejected_records"]), 2)


if __name__ == "__main__":
    unittest.main()