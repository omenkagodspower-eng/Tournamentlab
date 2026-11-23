def calculate_standings(teams, fixtures):
    standings = []

    for team in teams:
        stats = {
            "name": team,
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "gf": 0,
            "ga": 0,
            "gd": 0,
            "points": 0
        }

        standings.append(stats)

    for fixture in fixtures:
        if fixture["status"] != "played":
            continue

        home = fixture["home"]
        away = fixture["away"]

        home_score = fixture["home_score"]
        away_score = fixture["away_score"]

        for team in standings:
            if team["name"] == home:
                team["played"] += 1
                team["gf"] += home_score
                team["ga"] += away_score

                if home_score > away_score:
                    team["wins"] += 1
                    team["points"] += 3
                elif home_score == away_score:
                    team["draws"] += 1
                    team["points"] += 1
                else:
                    team["losses"] += 1

            elif team["name"] == away:
                team["played"] += 1
                team["gf"] += away_score
                team["ga"] += home_score

                if away_score > home_score:
                    team["wins"] += 1
                    team["points"] += 3
                elif away_score == home_score:
                    team["draws"] += 1
                    team["points"] += 1
                else:
                    team["losses"] += 1

    for team in standings:
        team["gd"] = team["gf"] - team["ga"]

    standings.sort(
        key=lambda team: (
            team["points"],
            team["gd"],
            team["gf"]
        ),
        reverse=True
    )

    return standings

def sort_standings(standings):
    standings.sort(
        key=lambda team: (
            team["points"],
            team["gd"],
            team["gf"]
        ),
        reverse=True
    )

    return standings