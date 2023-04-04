from collections import defaultdict
from operator import itemgetter

from team.models import TeamRanking

def ranking_generator():
    ranking = TeamRanking.objects.all()
    team_points = defaultdict(int)
    for game in ranking:
        if game.first_team_score == game.second_team_score:
            team_points[game.first_team] += 1
            team_points[game.second_team] += 1
        elif game.first_team_score > game.second_team_score:
            team_points[game.first_team] += 3
            team_points[game.second_team] += 0
        else:
            team_points[game.first_team] += 0
            team_points[game.second_team] += 3
    sorted_teams = sorted(team_points.items(), key=lambda x: (-x[1], x[0]))
    ranking_table = []
    for rank, (team_name, points) in enumerate(sorted_teams, start=1):
        ranking_table.append({
            'rank': rank,
            'team_name': team_name,
            'points': points,
        })
    return ranking_table