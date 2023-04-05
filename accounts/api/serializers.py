from rest_framework import serializers
from accounts.models import CustomUserModel


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields =["username", "email", "password"]