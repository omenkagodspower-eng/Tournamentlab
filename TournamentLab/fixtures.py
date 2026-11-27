def generate_fixtures(teams):
    if len(teams) < 4 or len(teams) > 8:
        return []

    fixtures = []
    fixture_id = 1

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):

            fixture = {
                "id": f"M{fixture_id:03d}",
                "home_id": teams[i]["id"],
                "away_id": teams[j]["id"],
                "status": "pending",
                "home_score": None,
                "away_score": None
            }

            fixtures.append(fixture)
            fixture_id += 1

    return fixtures


def record_result(fixtures, fixture_id, home_score, away_score):
    for fixture in fixtures:

        if fixture["id"] == fixture_id:

            if fixture["status"] != "pending":
                return False

            if not isinstance(home_score, int) or isinstance(home_score, bool):
                return False

            if not isinstance(away_score, int) or isinstance(away_score, bool):
                return False

            if home_score < 0 or away_score < 0:
                return False

            fixture["home_score"] = home_score
            fixture["away_score"] = away_score
            fixture["status"] = "played"

            return True

    return False