import unittest
from fixtures import record_result


class TestRecordResult(unittest.TestCase):

    def test_prevent_duplicate_match_result(self):
        fixtures = [
            {
                "id": 1,
                "home_score": None,
                "away_score": None,
                "status": "pending"
            }
        ]

        first_attempt = record_result(fixtures, 1, 3, 1)
        second_attempt = record_result(fixtures, 1, 2, 0)

        self.assertTrue(first_attempt)
        self.assertFalse(second_attempt)
    def test_reject_negative_score(self):
        fixtures = [
            {
                "id": 1,
                "home_score": None,
                "away_score": None,
                "status": "pending"
            }
        ]

        result = record_result(fixtures, 1, -1, 2)

        self.assertFalse(result)

    def test_reject_text_score(self):
        fixtures = [
            {
                "id": 1,
                "home_score": None,
                "away_score": None,
                "status": "pending"
            }
        ]

        result = record_result(fixtures, 1, "three", 2)

        self.assertFalse(result)
    def test_reject_invalid_fixture_id(self):
        fixtures = [
            {
                "id": 1,
                "home_score": None,
                "away_score": None,
                "status": "pending"
            }
        ]

        result = record_result(fixtures, 99, 2, 1)

        self.assertFalse(result)
if __name__ == "__main__":
    unittest.main()
