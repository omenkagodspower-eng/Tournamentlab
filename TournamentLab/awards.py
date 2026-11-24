def league_champion(standings):
    if not standings:
        return None

    return standings[0]

def top_scoring_team(standings):
    if not standings:
        return None

    return max(standings, key=lambda team: team["gf"])

def best_defensive_team(standings):
    if not standings:
        return None

    return min(standings, key=lambda team: team["ga"])

def highest_scoring_match(fixtures):
    played_fixtures = [
        fixture for fixture in fixtures
        if fixture["status"] == "played"
    ]

    if not played_fixtures:
        return None

    return max(
        played_fixtures,
        key=lambda fixture: fixture["home_score"] + fixture["away_score"]
    )