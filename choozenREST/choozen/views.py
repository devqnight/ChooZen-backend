from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from choozenREST.imdb import search_movie_by_title
from rest_framework.viewsets import ModelViewSet

from .models import Movie
from choozenREST.serializers import MovieSerializer

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # permission_classes = [IsAuthenticated]

@csrf_exempt
def search_movie(request):
    if request.method == 'POST':
        title_requested = request.POST.get('movie-title')
        result = search_movie_by_title(title_requested)
        return HttpResponse(result)

def get_csrf(request):
    return HttpResponse(request.COOKIES['csrftoken'])
