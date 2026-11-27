import unittest
from teams import register_team, can_start_tournament, validate_team_name


class TestTeams(unittest.TestCase):

    def setUp(self):
        self.teams = []

    def test_reject_empty_team_name(self):
        self.assertFalse(register_team("", self.teams))

    def test_reject_one_character_name(self):
        self.assertFalse(register_team("A", self.teams))

    def test_reject_name_longer_than_30_characters(self):
        self.assertFalse(register_team("A" * 31, self.teams))

    def test_accept_two_character_name(self):
        self.assertTrue(register_team("AB", self.teams))

    def test_accept_thirty_character_name(self):
        self.assertTrue(register_team("A" * 30, self.teams))

    def test_reject_duplicate_team_name(self):
        register_team("Phoenix", self.teams)
        self.assertFalse(register_team("Phoenix", self.teams))

    def test_reject_duplicate_with_different_case(self):
        register_team("Phoenix", self.teams)
        self.assertFalse(register_team("PHOENIX", self.teams))

    def test_remove_surrounding_spaces(self):
        register_team("  Phoenix  ", self.teams)
        self.assertEqual(self.teams[0]["name"], "Phoenix")

    def test_assign_team_id(self):
        register_team("Phoenix", self.teams)
        self.assertEqual(self.teams[0]["id"], "TM001")

    def test_reject_more_than_eight_teams(self):
        names = [
            "Phoenix", "Thunder", "Comets", "Rockets",
            "Lions", "Eagles", "Wolves", "Tigers"
        ]

        for name in names:
            self.assertTrue(register_team(name, self.teams))

        self.assertFalse(register_team("Dragons", self.teams))

    def test_tournament_requires_at_least_four_teams(self):
        self.assertFalse(can_start_tournament(self.teams))

        for name in ["Phoenix", "Thunder", "Comets"]:
            register_team(name, self.teams)

        self.assertFalse(can_start_tournament(self.teams))

        register_team("Rockets", self.teams)
        self.assertTrue(can_start_tournament(self.teams))


if __name__ == "__main__":
    unittest.main()