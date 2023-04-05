from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUserModel
from team.models import TeamRanking
from django.test import TestCase
from team.models.base_models import BaseModel
from team.models import TeamRanking
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from team.view.ranking import csv_upload, addRankingView, TeamRankingView, TeamRankingUpdateView, deleteRakingView

class ViewTest(TestCase):
    def setUp(self):
        self.user = CustomUserModel.objects.create_user(email='testuser@admin.com', password='testpass')
        self.client.login(email='testuser@admin.com', password='testpass')

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

    def test_ranking_list_view_template(self):
        url = reverse('ranking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ranking/ranking-list.html')

    def test_add_ranking_view_with_authentication(self):
        self.client.login(email='testuser@admin.com', password='testpass')
        url = reverse('add-ranking')
        data = {
            'first_team': 'Rebels A',
            'first_team_score': 1,
            'second_team': 'Fantastics B',
            'second_team_score': 0,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TeamRanking.objects.filter(first_team='Rebels A').exists())
        self.assertTrue(TeamRanking.objects.filter(second_team='Fantastics B').exists())
        ranking = TeamRanking.objects.get(first_team='Rebels A')
        self.assertEqual(ranking.first_team_score, 1)
        self.assertEqual(ranking.second_team_score, 0)

    def test_logout(self):
        self.client.logout()
        response = self.client.get(reverse('ranking-list'))
        self.assertEqual(response.status_code, 302)

class TeamRankingModelTest(TestCase):

    def setUp(self):
        self.team_ranking = TeamRanking.objects.create(
            first_team="Rebels A",
            first_team_score=10,
            second_team="Fantastics 2",
            second_team_score=8,
        )

    def test_string_representation(self):
        expected_str = 'Rebels A'
        self.assertEqual(str(self.team_ranking), expected_str)

    def test_teams_and_scores(self):
        self.assertEqual(self.team_ranking.first_team, "Rebels A")
        self.assertEqual(self.team_ranking.first_team_score, 10)
        self.assertEqual(self.team_ranking.second_team, "Fantastics 2")
        self.assertEqual(self.team_ranking.second_team_score, 8)

class TestUrls(SimpleTestCase):

    def test_csv_upload_url_resolves(self):
        url = reverse('upload_csv_file')
        self.assertEquals(resolve(url).func, csv_upload)

    def test_add_ranking_url_resolves(self):
        url = reverse('add-ranking')
        self.assertEquals(resolve(url).func, addRankingView)

    def test_ranking_list_url_resolves(self):
        url = reverse('ranking-list')
        self.assertEquals(resolve(url).func.view_class, TeamRankingView)

    def test_update_ranking_url_resolves(self):
        url = reverse('update-ranking', args=[1])
        self.assertEquals(resolve(url).func.view_class, TeamRankingUpdateView)

    def test_delete_ranking_url_resolves(self):
        url = reverse('ranking-delete', args=[1])
        self.assertEquals(resolve(url).func, deleteRakingView)