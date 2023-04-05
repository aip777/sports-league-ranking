from django.urls import path
from accounts.api.views import AuthView, RegisterAPIView
urlpatterns = [
    path('login-api/', AuthView.as_view()),
    path('register/', RegisterAPIView.as_view()),
]