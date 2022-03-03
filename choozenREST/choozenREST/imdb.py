import json
from unittest import result
import requests

url = "https://imdb-api.com/en/API/SearchTitle/k_whm9bxm3/"
api_keys = {"julien": "k_whm9bxm3", "kevin": "k_7co5uqo8", "quentin": "k_4nu9vksd", "martin": "k_h04ja628"}
payload = {}
headers= {}

def search_movie_by_title(movie_name):
  for (key, value) in api_keys.items():
    url = "https://imdb-api.com/en/API/SearchTitle/{}/{}".format(value, movie_name)
    response = requests.request("GET", url, headers=headers, data = payload)
    if not response.json().get("results") == None:
      return response.text

def advanced_search_movie(movie_imdb_id):
  for (key, value) in api_keys.items():
    url = "https://imdb-api.com/en/API/Title/{}/{}".format(value, movie_imdb_id)
    response = requests.request("GET", url, headers=headers, data = payload)
    if not response.json().get("title") == None:
      return response.json()    

def get_actor_list(movie_imdb_id):
  result = advanced_search_movie(movie_imdb_id)
  return result['actorList']

def search_actor_by_id(json, actor_imdb_id):
  json = json['actorList']
  for actor in json:
    if actor['id'] == actor_imdb_id:
      return actor

def get_character_name(movie_details_json, actor_imdb_id):
  result = search_actor_by_id(movie_details_json, actor_imdb_id)
  return result['asCharacter']
    