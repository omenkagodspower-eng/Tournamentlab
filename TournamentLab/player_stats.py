def calculate_player_goals(goal_scorers):
    player_goals = {}

    for player in goal_scorers:
        if player in player_goals:
            player_goals[player] += 1
        else:
            player_goals[player] = 1

    return player_goals

def top_goal_scorer(player_goals):
    if not player_goals:
        return None

    return max(player_goals, key=player_goals.get)

def rank_players(player_goals):
    return sorted(
        player_goals.items(),
        key=lambda player: player[1],
        reverse=True
    )