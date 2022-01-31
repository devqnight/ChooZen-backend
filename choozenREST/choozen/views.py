from django.http import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.core import serializers
from choozenREST.imdb import search_movie_by_title
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token

from .models import Movie, User
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
    try:
      token = request.COOKIES['csrftoken']
    except KeyError:
      token = get_token(request)
    return HttpResponse(token)

def is_authenticated(request):
    if request.method == 'POST':
      username = request.POST.get('username')
      token = request.POST.get('token')
      try:
        user = User.objects.get(username=username)
        token_db = Token.objects.get(key=token)
        if user.id == token_db.user_id:
          data = {'authenticated': True}
          data['id'] = user.id
          data['username'] = user.username
          data['first_name'] = user.first_name
          data['last_name'] = user.last_name
          data['email'] = user.email
          data['birthdate'] = user.birthdate
          data['last_login'] = user.last_login
          data['date_joined'] = user.date_joined
          data['is_superuser'] = user.is_superuser
          data['is_staff'] = user.is_staff
          data['is_active'] = user.is_active
          return JsonResponse(data, content_type='application/json', safe=False, status= 200)
        else:
          return HttpResponse(False, content_type='application/json', status=401)
      except (User.DoesNotExist, Token.DoesNotExist):
        return HttpResponse("The user or token does not exist", content_type='application/json', status=401)
    else:
      return HttpResponse("Only POST requests are allowed", content_type='application/json', status=405)