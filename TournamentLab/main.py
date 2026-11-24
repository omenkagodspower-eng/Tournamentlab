from standings import calculate_standings
from standings import calculate_standings, sort_standings
from fixtures import generate_fixtures, record_result
from teams import register_team, can_start_tournament

teams = []

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

if can_start_tournament(teams):
    fixtures = generate_fixtures(teams)

    print("\n=== Fixtures ===")
    for match in fixtures:
        print(match)

print("\n=== Record Match Result ===")

success = record_result(fixtures, 1, 3, 1)

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