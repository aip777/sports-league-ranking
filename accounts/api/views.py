from django.contrib.auth import authenticate
from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.views.generic import View
from rest_framework.authentication import SessionAuthentication

from accounts.models import CustomUserModel
from utils.response_maxin import ResponseWrapper
from .serializers import AccountSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

User = get_user_model()

class AuthView(APIView):
    permission_classes          = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return ResponseWrapper(data="You are already authenticated", status=400)
        data = request.data
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return ResponseWrapper(data=request.data.get('email'), msg="list", status=200)
        else:
            return ResponseWrapper(data='Email or password is incorrect', msg="list", status=401)


class RegisterAPIView(APIView):
    permission_classes          = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return ResponseWrapper(data="You are already authenticated", msg="list", status=401)
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        password2 = data.get("password")
        is_active =True
        qs = CustomUserModel.objects.filter(Q(username__iexact=username)| Q(email__iexact=email))

        if password != password2:
            return ResponseWrapper(data="Password must match", msg="list", status=401)

        if qs.exists():
            return ResponseWrapper(data="User already exists", msg="list", status=401)
        
        else:
            user = CustomUserModel.objects.create(username=username, email=email,is_active=is_active)
            user.set_password(password)
            user.save()
            return ResponseWrapper(data={'email':request.data.get('email'),'username':request.data.get('username')}, msg="list", status=200)