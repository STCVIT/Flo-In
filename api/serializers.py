from django.forms.fields import ImageField
from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from accounts.models import UserData

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username", "password")


class userDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ("user", "username", "url", "password")


class ImageSerializer(serializers.Serializer):
    image = ImageField(max_length=None, allow_empty_file=False)
