import unittest
import json
import os
import tempfile

from storage import save_tournament, load_tournament
from teams import register_team
from fixtures import generate_fixtures


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filepath = os.path.join(self.temp_dir.name, "tournament.json")

        self.teams = []

        for name in ["Thunder", "Comets", "Phoenix", "Rockets"]:
            register_team(name, self.teams)

        self.fixtures = generate_fixtures(self.teams)
        self.players = ["John", "David", "Peter"]

    def tearDown(self):
        self.temp_dir.cleanup()

    def save_data(self, teams=None, fixtures=None, players=None):
        data = {
            "schema_version": 1,
            "teams": self.teams if teams is None else teams,
            "fixtures": self.fixtures if fixtures is None else fixtures,
            "players": self.players if players is None else players
        }

        with open(self.filepath, "w") as file:
            json.dump(data, file)

    def test_save_and_load_tournament(self):
        save_tournament(
            self.filepath, self.teams, self.fixtures, self.players
        )

        teams, fixtures, players = load_tournament(self.filepath)

        self.assertEqual(teams, self.teams)
        self.assertEqual(fixtures, self.fixtures)
        self.assertEqual(players, self.players)

    def test_reject_unknown_fixture_team(self):
        fixtures = [dict(fixture) for fixture in self.fixtures]
        fixtures[0]["home_id"] = "TM999"

        self.save_data(fixtures=fixtures)

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)

    def test_reject_duplicate_team_names(self):
        teams = [dict(team) for team in self.teams]
        teams[1]["name"] = teams[0]["name"]

        self.save_data(teams=teams)

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)

    def test_reject_negative_scores(self):
        fixtures = [dict(fixture) for fixture in self.fixtures]
        fixtures[0].update({
            "status": "played",
            "home_score": -1,
            "away_score": 2
        })

        self.save_data(fixtures=fixtures)

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)

    def test_reject_invalid_fixture_status(self):
        fixtures = [dict(fixture) for fixture in self.fixtures]
        fixtures[0]["status"] = "cancelled"

        self.save_data(fixtures=fixtures)

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)

    def test_reject_duplicate_team_pairings(self):
        fixtures = [dict(fixture) for fixture in self.fixtures]
        fixtures[1]["home_id"] = fixtures[0]["home_id"]
        fixtures[1]["away_id"] = fixtures[0]["away_id"]

        self.save_data(fixtures=fixtures)

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)

    def test_reject_unsupported_schema_version(self):
        self.save_data()
        with open(self.filepath, "r") as file:
            data = json.load(file)

        data["schema_version"] = 2

        with open(self.filepath, "w") as file:
            json.dump(data, file)

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)

    def test_reject_empty_player_name(self):
        self.save_data(players=["John", ""])

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)

    def test_reject_duplicate_player_names(self):
        self.save_data(players=["John", "john"])

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)

    def test_reject_boolean_scores(self):
        fixtures = [dict(fixture) for fixture in self.fixtures]
        fixtures[0].update({
            "status": "played",
            "home_score": True,
            "away_score": 2
        })

        self.save_data(fixtures=fixtures)

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)

    def test_reject_incomplete_fixture_schedule(self):
        fixtures = self.fixtures[:-1]

        self.save_data(fixtures=fixtures)

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)

    def test_reject_invalid_json_structure(self):
        with open(self.filepath, "w") as file:
            json.dump([], file)

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)

    def test_reject_missing_required_data(self):
        data = {
            "schema_version": 1,
            "teams": self.teams
        }

        with open(self.filepath, "w") as file:
            json.dump(data, file)

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)

    def test_reject_pending_fixture_with_scores(self):
        fixtures = [dict(fixture) for fixture in self.fixtures]
        fixtures[0]["home_score"] = 2

        self.save_data(fixtures=fixtures)

        with self.assertRaises(ValueError):
            load_tournament(self.filepath)


if __name__ == "__main__":
    unittest.main()