import requests
import json

url = "https://imdb-api.com/en/API/SearchTitle/k_whm9bxm3/"
payload = {}
headers= {}

def search_movie_by_title(movie_name):
    response = requests.request("GET", url+movie_name, headers=headers, data = payload)
    return response.text
