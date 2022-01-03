from choozen.models import Movie, User
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'director', 'rating', 'genre']