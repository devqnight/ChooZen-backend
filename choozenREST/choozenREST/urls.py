"""choozenREST URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from choozen.views import MovieViewSet, search_movie, advanced_search_movie, get_csrf, is_authenticated, get_genres, save_movie, save_group, delete_group, join_group, get_groups, get_group, propose_movie, review_movie, get_movie_infos
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-choozen/', include(router.urls)),
    path('api-choozen/search/', search_movie, name='search_movie'),
    path('api-choozen/advanced_search/', advanced_search_movie, name='advanced_search_movie'),
    path('api-choozen-auth/', include('dj_rest_auth.urls')),
    path('api-choozen-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api-choozen/get_csrf/', get_csrf, name='get_csrf'),
    path('api-choozen-auth/is_authenticated/', is_authenticated, name='is_authenticated'),
    path('api-choozen/get_genres/', get_genres, name='get_genres'),
    path('api-choozen/save_movie/', save_movie, name='save_movie'),
    path('api-choozen/save_group/', save_group, name='save_group'),
    path('api-choozen/delete_group/', delete_group, name='delete_group'),
    path('api-choozen/join_group/', join_group, name='join_group'),
    path('api-choozen/get_groups/', get_groups, name='get_groups'),
    path('api-choozen/get_group/', get_group, name='get_group'),
    path('api-choozen/propose_movie/', propose_movie, name='get_group'),
    path('api-choozen/review_movie/', review_movie, name='review_movie'),
    path('api-choozen/getmovie/', get_movie_infos, name='get_movie_infos'),
]
