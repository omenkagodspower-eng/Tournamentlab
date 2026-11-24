import unittest

from awards import (
    league_champion,
    top_scoring_team,
    best_defensive_team,
    highest_scoring_match
)


class TestTournamentAwards(unittest.TestCase):

    def setUp(self):
        self.standings = [
            {"name": "Phoenix", "gf": 15, "ga": 5, "points": 12},
            {"name": "Comets", "gf": 10, "ga": 3, "points": 10},
            {"name": "Thunder", "gf": 8, "ga": 7, "points": 6}
        ]

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
                "home": "Thunder",
                "away": "Rockets",
                "status": "played",
                "home_score": 4,
                "away_score": 2
            },
            {
                "id": 3,
                "home": "Phoenix",
                "away": "Thunder",
                "status": "pending"
            }
        ]

    def test_league_champion(self):
        self.assertEqual(league_champion(self.standings)["name"], "Phoenix")

    def test_top_scoring_team(self):
        self.assertEqual(top_scoring_team(self.standings)["name"], "Phoenix")

    def test_best_defensive_team(self):
        self.assertEqual(best_defensive_team(self.standings)["name"], "Comets")

    def test_highest_scoring_match(self):
        match = highest_scoring_match(self.fixtures)
        self.assertEqual(match["home"], "Thunder")
        self.assertEqual(match["away"], "Rockets")

    def test_league_champion_empty_standings(self):
        self.assertIsNone(league_champion([]))

    def test_top_scoring_team_empty_standings(self):
        self.assertIsNone(top_scoring_team([]))

    def test_best_defensive_team_empty_standings(self):
        self.assertIsNone(best_defensive_team([]))

    def test_highest_scoring_match_without_played_matches(self):
        self.assertIsNone(highest_scoring_match([
            {"id": 1, "home": "Phoenix", "away": "Comets", "status": "pending"}
        ]))


if __name__ == "__main__":
    unittest.main()