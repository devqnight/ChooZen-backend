import json
from unittest import result
from choozenREST.serializers import MovieSerializer, PersonSerializer
from choozen.models import Movie, Person, Directed, Played, Genre, HasGenre
import requests

url = "https://imdb-api.com/en/API/SearchTitle/k_whm9bxm3/"
api_keys = {"julien": "k_whm9bxm3", "kevin": "k_7co5uqo8", "quentin": "k_4nu9vksd", "martin": "k_h04ja628"}
payload = {}
headers= {}

def search_movie_by_title(movie_name):
  for (key, value) in api_keys.items():
    url = "https://imdb-api.com/en/API/SearchTitle/{}/{}".format(value, movie_name)
    response = requests.request("GET", url, headers=headers, data = payload)
    if response.json().get("results") != None:
      return response.text

def advanced_search_movie_id(movie_imdb_id):
  for (key, value) in api_keys.items():
    url = "https://imdb-api.com/en/API/Title/{}/{}".format(value, movie_imdb_id)
    response = requests.request("GET", url, headers=headers, data = payload)
    if response.json().get("title") != None:
      return response.json()

def advanced_search_movie_by_title(movie_name):
  for (key, value) in api_keys.items():
    url = "https://imdb-api.com/en/API/AdvancedSearch/{}?title={}".format(value, movie_name)
    response = requests.request("GET", url, headers=headers, data = payload)
    if response.json().get("results") != None:
      return response.text

def get_actor_list(movie_imdb_id):
  result = advanced_search_movie_id(movie_imdb_id)
  return result['actorList']

def search_actor_by_id(json, actor_imdb_id):
  json = json['actorList']
  for actor in json:
    if actor['id'] == actor_imdb_id:
      return actor

def get_character_name(movie_details_json, actor_imdb_id):
  result = search_actor_by_id(movie_details_json, actor_imdb_id)
  return result['asCharacter']

def get_actor_picture(movie_details_json, actor_imdb_id):
  result = search_actor_by_id(movie_details_json, actor_imdb_id)
  return result['image']

def get_saved_movie_infos(_imdb_id):
  movie_object = Movie.objects.get(imdb_id=_imdb_id)
  directors_objects = Directed.objects.filter(movie_id=_imdb_id)
  directors = []
  for director in directors_objects:
    director_id = director.director_id
    director = Person.objects.get(imdb_id=director_id)
    director_serializer = PersonSerializer(director)
    directors.append(director_serializer.data)
  actors_objects = Played.objects.filter(movie_id=_imdb_id)
  actors = []
  for actor in actors_objects:
    actor_id = actor.actor_id
    person = Person.objects.get(imdb_id=actor_id)
    actor_serializer = PersonSerializer(person)
    data = actor_serializer.data
    data['character'] = actor.character_name
    actors.append(data)
  genres_objects = HasGenre.objects.filter(movie_id=_imdb_id)
  genres = []
  for genre in genres_objects:
    genre_id = genre.genre_id
    genre = Genre.objects.get(id=genre_id)
    genres.append(genre.type)
  movie_serializer = MovieSerializer(movie_object).data
  movie_serializer['directors'] = directors
  movie_serializer['actors'] = actors
  movie_serializer['genres'] = genres
  return movie_serializer

def save_movie_in_db(imdb_id):
  movie_data = advanced_search_movie_id(imdb_id)
  serializer = MovieSerializer(
    data={
      'imdb_id': movie_data['id'],
      'title': movie_data['title'],
      'length': movie_data['runtimeMins'],
      'plot': movie_data['plot'],
      'content_rating': movie_data['contentRating'],
      'imdb_rating': movie_data['imDbRating'],
      'poster_url': movie_data['image'],
      'release_date': movie_data['releaseDate'],
      'year': movie_data['year'],
      'type': movie_data['type'],
      'runtimeStr': movie_data['runtimeStr'],
    })
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
        actor_picture = get_actor_picture(movie_data, id)
        person = Person.objects.create(imdb_id=id, full_name=name, picture_url=actor_picture)
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
      return serializer
  else:
    return serializer
