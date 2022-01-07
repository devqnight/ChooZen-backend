from django.http import response
from django.views.decorators.csrf import csrf_exempt
from choozenREST.imdb import search_movie_by_title
from rest_framework.mixins import (CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView

from .models import Movie
from choozenREST.serializers import MovieSerializer

class MovieViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

@csrf_exempt
def search_movie(request):
    if request.method == 'POST':
        title_requested = request.POST.get('movie-title')
        result = search_movie_by_title(title_requested)
        return response.HttpResponse(result)
