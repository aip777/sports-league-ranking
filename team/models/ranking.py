from team.models.base_models import BaseModel
from django.db import models
class TeamRanking(BaseModel):
    first_team = models.CharField(max_length=100)
    first_team_score = models.IntegerField()
    second_team = models.CharField(max_length=100)
    second_team_score = models.IntegerField()

    def __str__(self):
        return str(self.first_team)



