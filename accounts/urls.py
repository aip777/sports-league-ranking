from django.urls import path, include
from .views import *

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-user/', register_view, name='add-user'),
]