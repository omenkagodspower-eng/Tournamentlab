import json


def save_tournament(filepath, teams, fixtures, players):
    data = {
        "schema_version": 1,
        "teams": teams,
        "fixtures": fixtures,
        "players": players
    }

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


def load_tournament(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Save file must contain a JSON object.")

    if data.get("schema_version") != 1:
        raise ValueError("Unsupported save file version.")

    required_keys = ["teams", "fixtures", "players"]

    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required data: {key}")

    if not isinstance(data["teams"], list):
        raise ValueError("Teams must be a list.")

    if not isinstance(data["fixtures"], list):
        raise ValueError("Fixtures must be a list.")

    if not isinstance(data["players"], list):
        raise ValueError("Players must be a list.")

    teams = data["teams"]
    fixtures = data["fixtures"]
    players = data["players"]

    if len(teams) > 8:
        raise ValueError("A tournament cannot have more than 8 teams.")

    if fixtures and len(teams) < 4:
        raise ValueError("A tournament must have at least 4 teams.")

    team_ids = set()
    team_names = set()

    for team in teams:
        if not isinstance(team, dict):
            raise ValueError("Invalid team record.")

        if "id" not in team or "name" not in team:
            raise ValueError("Team record is missing required fields.")

        team_id = team["id"]
        team_name = team["name"]

        if not isinstance(team_id, str) or not isinstance(team_name, str):
            raise ValueError("Team ID and name must be strings.")

        if not team_name.strip() or not 2 <= len(team_name) <= 30:
            raise ValueError("Invalid team name.")

        if team_name != team_name.strip():
            raise ValueError("Team names must not contain surrounding spaces.")

        expected_id = f"TM{len(team_ids) + 1:03d}"

        if team_id != expected_id:
            raise ValueError("Invalid or out-of-sequence team ID.")

        if team_name.casefold() in team_names:
            raise ValueError("Duplicate team name.")

        team_ids.add(team_id)
        team_names.add(team_name.casefold())

    fixture_ids = set()
    team_pairs = set()

    for fixture in fixtures:
        if not isinstance(fixture, dict):
            raise ValueError("Invalid fixture record.")

        required_fields = [
            "id", "home_id", "away_id",
            "status", "home_score", "away_score"
        ]

        for field in required_fields:
            if field not in fixture:
                raise ValueError(f"Fixture is missing {field}.")

        fixture_id = fixture["id"]
        home_id = fixture["home_id"]
        away_id = fixture["away_id"]
        status = fixture["status"]
        home_score = fixture["home_score"]
        away_score = fixture["away_score"]

        if not all(isinstance(value, str) for value in
                   [fixture_id, home_id, away_id]):
            raise ValueError("Fixture IDs must be strings.")

        expected_id = f"M{len(fixture_ids) + 1:03d}"

        if fixture_id != expected_id:
            raise ValueError("Invalid or out-of-sequence fixture ID.")

        if home_id not in team_ids or away_id not in team_ids:
            raise ValueError("Fixture references an unknown team.")

        if home_id == away_id:
            raise ValueError("A team cannot play against itself.")

        pair = frozenset([home_id, away_id])

        if pair in team_pairs:
            raise ValueError("Duplicate team pairing.")

        if status not in ["pending", "played"]:
            raise ValueError("Invalid fixture status.")

        if status == "pending":
            if home_score is not None or away_score is not None:
                raise ValueError("Pending fixtures cannot have scores.")

        if status == "played":
            for score in [home_score, away_score]:
                if not isinstance(score, int) or isinstance(score, bool):
                    raise ValueError("Scores must be integers.")

                if score < 0:
                    raise ValueError("Scores cannot be negative.")

        fixture_ids.add(fixture_id)
        team_pairs.add(pair)

    if fixtures:
        expected_fixtures = len(teams) * (len(teams) - 1) // 2

        if len(fixtures) != expected_fixtures:
            raise ValueError("Incomplete round-robin fixture schedule.")

    player_names = set()

    for player in players:
        if not isinstance(player, str):
            raise ValueError("Player names must be strings.")

        if not player.strip():
            raise ValueError("Player names cannot be empty.")

        if player != player.strip():
            raise ValueError("Player names must not contain surrounding spaces.")

        if player.casefold() in player_names:
            raise ValueError("Duplicate player name.")

        player_names.add(player.casefold())

    return teams, fixtures, players