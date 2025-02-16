from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()
    message = serializers.CharField()