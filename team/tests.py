from django.test import TestCase
from django.urls import reverse

from team.models import TeamRanking


# Create your tests here.


class ListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        result = [{"Crazy Ones":3, "Rebels": 3},
                  {"Fantastics": 1, "FC Super": 0},
                  {"Crazy Ones": 1, "FC Super": 1},
                  {"Fantastics": 3, "Rebels": 1},
                  {"Crazy Ones": 4, "Misfits": 0},
                  ]
        for _result in result:
            TeamRanking.objects.create(
                first_team=list(_result)[0], first_team_score=int(list(_result.values())[0]), second_team=list(_result)[1],
                second_team_score=int(list(_result.values())[1])
            )

    def test_url_exists(self):
        response = self.client.get("ranking-list")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('ranking-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('ranking-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ranking/ranking-list.html')
