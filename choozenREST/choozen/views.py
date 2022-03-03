from choozenREST.imdb import search_movie_by_title, advanced_search_movie, get_character_name
from choozenREST.serializers import CustomGenreSerializer, MovieSerializer
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet

from .models import Directed, Genre, HasGenre, Movie, Person, Played, User

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

def save_movie(request):
  if request.method == 'POST':
    imdb_id = request.POST.get('imdb_id')
    try:
      movie = Movie.objects.get(imdb_id=imdb_id)
      data = MovieSerializer(movie).data
      return JsonResponse(data, content_type='application/json', safe=False, status=409)
    except Movie.DoesNotExist:
      movie_data = advanced_search_movie(imdb_id)
      print(movie_data)
      serializer = MovieSerializer(
        data={
          'imdb_id': movie_data['id'],
          'title': movie_data['title'],
          'year': movie_data['year'],
          'length': movie_data['runtimeMins'],
          'plot': movie_data['plot'],
          'content_rating': movie_data['contentRating'],
          'imdb_rating': movie_data['imDbRating'],
          'poster_url': movie_data['image'],
          'release_date': movie_data['releaseDate'],
        })
      print(serializer)
      if serializer.is_valid():
        serializer.save()
        movie_obj = Movie.objects.get(imdb_id=imdb_id)

        # add directors
        director_list = movie_data['directorList']
        for director in director_list:
          id = director['id']
          name = director['name']
          try:
            person = Person.objects.get(imdb_id=id)
          except Person.DoesNotExist:
            person = Person.objects.create(imdb_id=id, full_name=name)
          Directed.objects.create(movie=movie_obj, director=person)

        # add main actors
        actor_list = movie_data['starList']
        for actor in actor_list:
          id = actor['id']
          name = actor['name']
          try:
            person = Person.objects.get(imdb_id=id)
          except Person.DoesNotExist:
            person = Person.objects.create(imdb_id=id, full_name=name)
          carac_name = get_character_name(movie_data, id)
          Played.objects.create(movie=movie_obj, actor=person, character_name=carac_name)

        # add genres
        genre_list = movie_data['genreList']
        for genre in genre_list:
          genre_name = genre['value']
          try:
            genre_obj = Genre.objects.get(type=genre_name)
          except Genre.DoesNotExist:
            genre_obj = Genre.objects.create(type=genre_name)
          HasGenre.objects.create(movie=movie_obj, genre=genre_obj)
        return JsonResponse(serializer.data, content_type='application/json', safe=False, status=201)
      return JsonResponse(serializer.errors, status=400, content_type='application/json')
  else:
    return HttpResponse("Only POST requests are allowed", content_type='application/json', status=405)

def get_genres(request):
    if request.method == 'GET':
        genres = Genre.objects.all()
        data = CustomGenreSerializer(genres, many=True).data
        return JsonResponse(data, content_type='application/json', safe=False, status=200)
    else:
        return HttpResponse("Only GET requests are allowed", content_type='application/json', status=405)
