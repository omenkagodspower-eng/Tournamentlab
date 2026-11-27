import json
from storage import save_tournament, load_tournament
from player_stats import calculate_player_goals, top_goal_scorer, rank_players
from awards import league_champion, top_scoring_team, best_defensive_team, highest_scoring_match
from standings import calculate_standings, sort_standings
from fixtures import generate_fixtures, record_result
from teams import register_team, can_start_tournament
from statistics import total_matches, matches_played, matches_remaining, total_goals, average_goals_per_match
teams = []
players = []
fixtures = []
goal_scorers = []

SAVE_FILE = "tournament.json"
loaded = False

print("=== TournamentLab ===")
print("1. Start a new tournament")
print("2. Load a saved tournament")

choice = input("Choose an option (1 or 2): ").strip()

if choice == "2":
    try:
        teams, fixtures, players = load_tournament(SAVE_FILE)
        loaded = True
        print("\nTournament loaded successfully!")

    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        print("\nCould not load tournament:", error)

elif choice != "1":
    print("Invalid option. Starting a new tournament.")

while not loaded and len(teams) < 8:
    name = input("Enter team name (or 'done' to finish): ").strip()

    if name.lower() == "done":
        if len(teams) >= 4:
            break
        print("You must register at least 4 teams!")
        continue

    if register_team(name, teams):
        print("Team registered successfully!\n")
    else:
        print("Invalid name or duplicate team.\n")

print("\nRegistered teams:", teams)
print("Can tournament start?", can_start_tournament(teams))
print("\n=== Player Registration ===")

while not loaded:
    player_name = input("Enter player name (or 'done' to finish): ").strip()

    if player_name.lower() == "done":
        break

    if player_name and player_name not in players:
        players.append(player_name)
        print("Player registered successfully!\n")
    else:
        print("Invalid name or duplicate player.\n")

if not loaded and can_start_tournament(teams):
    fixtures = generate_fixtures(teams)

    print("\n=== Fixtures ===")
    for match in fixtures:
        print(match)

print("\n=== Record Match Result ===")

team_lookup = {
    team["id"]: team["name"] for team in teams
}

pending_fixtures = [
    fixture for fixture in fixtures
    if fixture["status"] == "pending"
]

success = False
player_goals = {}

if pending_fixtures:
    print("\nPending matches:")

    for fixture in pending_fixtures:
        print(
            f"{fixture['id']}: "
            f"{team_lookup[fixture['home_id']]} vs "
            f"{team_lookup[fixture['away_id']]}"
        )

    fixture_id = input("\nEnter fixture ID to record: ").strip()

    selected_fixture = next(
        (f for f in pending_fixtures if f["id"] == fixture_id),
        None
    )

    if selected_fixture:
        try:
            home_score = int(input("Enter home score: "))
            away_score = int(input("Enter away score: "))

            success = record_result(
                fixtures, fixture_id, home_score, away_score
            )

        except ValueError:
            print("Invalid score. Please enter whole numbers.")

        if success:
            print("Match result recorded successfully!")

            print("\nRegistered players:")
            for player in players:
                print(player)

            try:
                scorer_count = int(
                    input("How many goals were scored in this match?: ")
                )

                for i in range(scorer_count):
                    while True:
                        scorer = input(
                            f"Enter scorer {i + 1}: "
                        ).strip()

                        if scorer in players:
                            goal_scorers.append(scorer)
                            break

                        print("Player not registered. Try again.")

                player_goals = calculate_player_goals(goal_scorers)

            except ValueError:
                print("Invalid goal count.")

        else:
            print("Could not record match result.")

    else:
        print("Invalid fixture ID.")

else:
    print("There are no pending matches.")

if success:
    print("\nUpdated Fixture:")
    print(selected_fixture)
print("\n=== LEAGUE STANDINGS ===")

standings = calculate_standings(teams, fixtures)

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
            f"{team_lookup[fixture['home_id']]} "
            f"{fixture['home_score']} - "
            f"{fixture['away_score']} "
            f"{team_lookup[fixture['away_id']]}"
        )

print("\n=== FIXTURES LIST ===")

for fixture in fixtures:
    print(
        f"{fixture['id']}: "
        f"{team_lookup[fixture['home_id']]} vs "
        f"{team_lookup[fixture['away_id']]} - "
        f"{fixture['status'].title()}"
    )

print("\n=== TOURNAMENT STATISTICS ===")

print("Total matches:", total_matches(fixtures))
print("Matches played:", matches_played(fixtures))
print("Matches remaining:", matches_remaining(fixtures))
print("Total goals scored:", total_goals(fixtures))
print("Average goals per match:", average_goals_per_match(fixtures))

print("\n=== TOURNAMENT AWARDS ===")

champion = league_champion(standings, fixtures)
top_scorer = top_scoring_team(standings)
best_defence = best_defensive_team(standings)
highest_match = highest_scoring_match(fixtures)

if champion:
    print("League champion:", champion["name"])
else:
    print("Tournament in progress. No champion yet.")

if top_scorer:
    print("Top-scoring team:", top_scorer["name"])

if best_defence:
    print("Best defensive team:", best_defence["name"])

if highest_match:
    print(
        "Highest-scoring match:",
        f"{team_lookup[highest_match['home_id']]} "
        f"{highest_match['home_score']} - "
        f"{highest_match['away_score']} "
        f"{team_lookup[highest_match['away_id']]}"
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

print("\n=== SAVE TOURNAMENT ===")

save_choice = input("Save tournament? (yes/no): ").strip().lower()

if save_choice == "yes":
    save_tournament(SAVE_FILE, teams, fixtures, players)
    print("Tournament saved successfully!")
else:
    print("Tournament not saved.")