def total_matches(fixtures):
    return len(fixtures)
def matches_played(fixtures):
    return sum(1 for fixture in fixtures if fixture["status"] == "played")
def matches_remaining(fixtures):
    return total_matches(fixtures) - matches_played(fixtures)
def total_goals(fixtures):
    return sum(
        fixture["home_score"] + fixture["away_score"]
        for fixture in fixtures
        if fixture["status"] == "played"
    )
def average_goals_per_match(fixtures):
    played = matches_played(fixtures)

    if played == 0:
        return 0

    return total_goals(fixtures) / played