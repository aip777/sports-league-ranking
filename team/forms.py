from django import forms

from team.models import TeamRanking


class RankingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RankingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = TeamRanking
        fields = (
            "id",
            "first_team",
            "first_team_score",
            "second_team",
            "second_team_score",
        )
