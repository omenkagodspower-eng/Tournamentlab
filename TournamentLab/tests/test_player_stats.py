import unittest

from player_stats import (
    calculate_player_goals,
    top_goal_scorer,
    rank_players
)


class TestPlayerStats(unittest.TestCase):

    def test_calculate_player_goals(self):
        scorers = ["John", "Peter", "John", "David"]
        result = calculate_player_goals(scorers)

        self.assertEqual(result, {
            "John": 2,
            "Peter": 1,
            "David": 1
        })

    def test_top_goal_scorer(self):
        goals = {"John": 2, "Peter": 1, "David": 4}

        self.assertEqual(top_goal_scorer(goals), "David")

    def test_top_goal_scorer_empty(self):
        self.assertIsNone(top_goal_scorer({}))

    def test_rank_players(self):
        goals = {"John": 2, "Peter": 1, "David": 4}

        self.assertEqual(rank_players(goals), [
            ("David", 4),
            ("John", 2),
            ("Peter", 1)
        ])

    def test_calculate_player_goals_empty(self):
        self.assertEqual(calculate_player_goals([]), {})


if __name__ == "__main__":
    unittest.main()
