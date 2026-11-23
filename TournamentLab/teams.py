def validate_team_name(name):
    name = name.strip()

    if name == "":
        return False

    return True

def register_team(name, teams):
    name = name.strip()

    if not validate_team_name(name):
        return False

    for team in teams:
        if team.lower() == name.lower():
            return False

    if len(teams) >= 8:
        return False

    teams.append(name)
    return True

def can_start_tournament(teams):
    if len(teams) < 4:
        return False

    return True
