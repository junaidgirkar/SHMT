from rest_framework import serializers
from accounts.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "active",
            "staff",
            "admin",
        ]

class LoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    def get_token(self, obj):
        return Token.objects.get(user=obj).key
    class Meta:
        model = User

        fields = ['id', 'token', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

