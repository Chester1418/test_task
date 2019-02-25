from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post
from rest_framework.validators import UniqueValidator


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True)

    class Meta:
        model = User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'author')
