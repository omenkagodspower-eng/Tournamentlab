import unittest
from standings import calculate_standings, sort_standings


class TestCalculateStandings(unittest.TestCase):

    def test_calculate_win_and_loss(self):
        teams = ["Phoenix", "Comets"]

        fixtures = [
            {
                "home": "Phoenix",
                "away": "Comets",
                "home_score": 3,
                "away_score": 1,
                "status": "played"
            }
        ]

        standings = calculate_standings(teams, fixtures)

        phoenix = standings[0]
        comets = standings[1]

        self.assertEqual(phoenix["wins"], 1)
        self.assertEqual(phoenix["points"], 3)
        self.assertEqual(phoenix["gd"], 2)

        self.assertEqual(comets["losses"], 1)
        self.assertEqual(comets["points"], 0)
        self.assertEqual(comets["gd"], -2)

    def test_calculate_draw(self):
        teams = ["Phoenix", "Comets"]

        fixtures = [
            {
                "home": "Phoenix",
                "away": "Comets",
                "home_score": 2,
                "away_score": 2,
                "status": "played"
            }
        ]

        standings = calculate_standings(teams, fixtures)

        for team in standings:
            self.assertEqual(team["draws"], 1)
            self.assertEqual(team["points"], 1)

    def test_ignore_pending_fixtures(self):
        teams = ["Phoenix", "Comets"]

        fixtures = [
            {
                "home": "Phoenix",
                "away": "Comets",
                "home_score": 3,
                "away_score": 1,
                "status": "pending"
            }
        ]

        standings = calculate_standings(teams, fixtures)

        for team in standings:
            self.assertEqual(team["played"], 0)
            self.assertEqual(team["points"], 0)
    def test_empty_teams(self):
        teams = []
        fixtures = []

        standings = calculate_standings(teams, fixtures)

        self.assertEqual(standings, [])

    def test_teams_without_fixtures(self):
        teams = ["Phoenix", "Comets"]
        fixtures = []

        standings = calculate_standings(teams, fixtures)

        self.assertEqual(len(standings), 2)

        for team in standings:
            self.assertEqual(team["played"], 0)
            self.assertEqual(team["points"], 0)
            self.assertEqual(team["wins"], 0)

class TestSortStandings(unittest.TestCase):

    def test_sort_by_points(self):
        standings = [
            {"name": "Comets", "points": 3, "gd": 1, "gf": 2},
            {"name": "Phoenix", "points": 9, "gd": 4, "gf": 6},
            {"name": "Thunder", "points": 6, "gd": 2, "gf": 3}
        ]

        sorted_teams = sort_standings(standings)

        self.assertEqual(sorted_teams[0]["name"], "Phoenix")
        self.assertEqual(sorted_teams[1]["name"], "Thunder")
        self.assertEqual(sorted_teams[2]["name"], "Comets")
    def test_sort_by_goal_difference(self):
        standings = [
            {"name": "Comets", "points": 6, "gd": 2, "gf": 5},
            {"name": "Phoenix", "points": 6, "gd": 5, "gf": 7}
        ]

        sorted_teams = sort_standings(standings)

        self.assertEqual(sorted_teams[0]["name"], "Phoenix")
        self.assertEqual(sorted_teams[1]["name"], "Comets")

    def test_sort_by_goals_scored(self):
        standings = [
            {"name": "Comets", "points": 6, "gd": 3, "gf": 5},
            {"name": "Phoenix", "points": 6, "gd": 3, "gf": 8}
        ]

        sorted_teams = sort_standings(standings)

        self.assertEqual(sorted_teams[0]["name"], "Phoenix")
        self.assertEqual(sorted_teams[1]["name"], "Comets")

if __name__ == "__main__":
    unittest.main()
