from django.urls import path
from team.view.ranking import (
    csv_upload,
    addRankingView,
    rankinglistView,
    deleteRakingView,
    updateRankingView,
)
from .document.document_view import error_log

urlpatterns = [
    path("", csv_upload, name="upload_csv_file"),
    path("error-log/", error_log, name="error_log"),
    path("add-ranking/", addRankingView, name="add-ranking"),
    path("list-ranking/", rankinglistView, name="ranking-list"),
    path("update-ranking/<int:id>/", updateRankingView, name="update-ranking"),
    path("delete-ranking/<int:id>/", deleteRakingView, name="ranking-delete"),
]
