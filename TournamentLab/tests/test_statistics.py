import unittest

from statistics import (
    total_matches,
    matches_played,
    matches_remaining,
    total_goals,
    average_goals_per_match
)


class TestTournamentStatistics(unittest.TestCase):

    def setUp(self):
        self.fixtures = [
            {
                "id": 1,
                "home": "Phoenix",
                "away": "Comets",
                "status": "played",
                "home_score": 3,
                "away_score": 1
            },
            {
                "id": 2,
                "home": "Phoenix",
                "away": "Thunder",
                "status": "pending"
            },
            {
                "id": 3,
                "home": "Comets",
                "away": "Thunder",
                "status": "played",
                "home_score": 2,
                "away_score": 2
            }
        ]

    def test_total_matches(self):
        self.assertEqual(total_matches(self.fixtures), 3)

    def test_matches_played(self):
        self.assertEqual(matches_played(self.fixtures), 2)

    def test_matches_remaining(self):
        self.assertEqual(matches_remaining(self.fixtures), 1)

    def test_total_goals(self):
        self.assertEqual(total_goals(self.fixtures), 8)

    def test_average_goals_per_match(self):
        self.assertEqual(average_goals_per_match(self.fixtures), 4.0)

    def test_average_goals_with_no_matches_played(self):
        self.assertEqual(average_goals_per_match([]), 0)


if __name__ == "__main__":
    unittest.main()