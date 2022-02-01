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
