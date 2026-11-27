def validate_team_name(name, teams):
    name = name.strip()

    if len(name) < 2 or len(name) > 30:
        return False

    for team in teams:
        if team["name"].casefold() == name.casefold():
            return False

    return True


def register_team(name, teams):
    name = name.strip()

    if not validate_team_name(name, teams):
        return False

    if len(teams) >= 8:
        return False

    team_id = f"TM{len(teams) + 1:03d}"

    team = {
        "id": team_id,
        "name": name
    }

    teams.append(team)
    return True


def can_start_tournament(teams):
    return len(teams) >= 4