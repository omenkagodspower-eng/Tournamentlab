from player_stats import calculate_player_goals, top_goal_scorer, rank_players
from awards import league_champion, top_scoring_team, best_defensive_team, highest_scoring_match
from standings import calculate_standings, sort_standings
from fixtures import generate_fixtures, record_result
from teams import register_team, can_start_tournament
from statistics import total_matches, matches_played, matches_remaining, total_goals, average_goals_per_match
teams = []
players = []

print("=== TournamentLab ===")
print("Register 4 to 8 teams.\n")

while len(teams) < 4:
    name = input("Enter team name: ")

    if register_team(name, teams):
        print("Team registered successfully!\n")
    else:
        print("Invalid name or duplicate team.\n")

print("\nRegistered teams:", teams)
print("Can tournament start?", can_start_tournament(teams))
print("\n=== Player Registration ===")

while True:
    player_name = input("Enter player name (or 'done' to finish): ").strip()

    if player_name.lower() == "done":
        break

    if player_name and player_name not in players:
        players.append(player_name)
        print("Player registered successfully!\n")
    else:
        print("Invalid name or duplicate player.\n")

if can_start_tournament(teams):
    fixtures = generate_fixtures(teams)

    print("\n=== Fixtures ===")
    for match in fixtures:
        print(match)

print("\n=== Record Match Result ===")

success = record_result(fixtures, 1, 3, 1)
goal_scorers = []

print("\nRegistered players:")

for player in players:
    print(player)

scorer_count = int(input("How many goals were scored in this match?: "))

for i in range(scorer_count):
    while True:
        scorer = input(f"Enter scorer {i + 1}: ").strip()

        if scorer in players:
            goal_scorers.append(scorer)
            break
        else:
            print("Player not registered! Please enter a registered player.")

player_goals = calculate_player_goals(goal_scorers)
if success:
    print("Match result recorded successfully!")
else:
    print("Could not record match result.")

print("\nUpdated Fixture:")
print(fixtures[0])
print("\n=== League Standings ===")

table = calculate_standings(teams, fixtures)
table = sort_standings(table)

standings = calculate_standings(teams, fixtures)

print("\n=== LEAGUE TABLE ===")

print(
    f"{'POS':<5}"
    f"{'TEAM':<12}"
    f"{'P':<5}"
    f"{'W':<5}"
    f"{'D':<5}"
    f"{'L':<5}"
    f"{'GF':<5}"
    f"{'GA':<5}"
    f"{'GD':<5}"
    f"{'PTS':<5}"
)

for position, team in enumerate(standings, start=1):
    print(
        f"{position:<5}"
        f"{team['name']:<12}"
        f"{team['played']:<5}"
        f"{team['wins']:<5}"
        f"{team['draws']:<5}"
        f"{team['losses']:<5}"
        f"{team['gf']:<5}"
        f"{team['ga']:<5}"
        f"{team['gd']:<5}"
        f"{team['points']:<5}"
    )

print("\n=== MATCH RESULTS ===")

for fixture in fixtures:
    if fixture["status"] == "played":
        print(
            f"{fixture['home']} "
            f"{fixture['home_score']} - "
            f"{fixture['away_score']} "
            f"{fixture['away']}"
        )

print("\n=== FIXTURES LIST ===")

for fixture in fixtures:
    print(f"{fixture['home']} vs {fixture['away']} - {fixture['status'].title()}")

print("\n=== TOURNAMENT STATISTICS ===")

print("Total matches:", total_matches(fixtures))
print("Matches played:", matches_played(fixtures))
print("Matches remaining:", matches_remaining(fixtures))
print("Total goals scored:", total_goals(fixtures))
print("Average goals per match:", average_goals_per_match(fixtures))
print("\n=== TOURNAMENT AWARDS ===")

champion = league_champion(standings)
top_scorer = top_scoring_team(standings)
best_defence = best_defensive_team(standings)
highest_match = highest_scoring_match(fixtures)

if champion:
    print("League champion:", champion["name"])

if top_scorer:
    print("Top-scoring team:", top_scorer["name"])

if best_defence:
    print("Best defensive team:", best_defence["name"])

if highest_match:
    print(
        "Highest-scoring match:",
        f"{highest_match['home']} {highest_match['home_score']} - "
        f"{highest_match['away_score']} {highest_match['away']}"
    )
else:
    print("Highest-scoring match: No matches played yet.")

print("\n=== PLAYER STATISTICS ===")

for player, goals in rank_players(player_goals):
    word = "goal" if goals == 1 else "goals"
    print(f"{player}: {goals} {word}")

top_player = top_goal_scorer(player_goals)

if top_player:
    print("Top goal scorer:", top_player)
