from django.contrib import admin
from team.models import TeamRanking

class AdminTeamRanking(admin.ModelAdmin):
    list_display = (
        "first_team",
        "first_team_score",
        "second_team",
        "second_team_score",
    )
admin.site.register(TeamRanking, AdminTeamRanking)

