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
from choozen.views import MovieViewSet, search_movie, get_csrf, is_authenticated
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-choozen/', include(router.urls)),
    path('api-choozen/search/', search_movie, name='search_movie'),
    path('api-choozen-auth/', include('dj_rest_auth.urls')),
    path('api-choozen-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api-choozen/get_csrf/', get_csrf, name='get_csrf'),
    path('api-choozen-auth/is_authenticated/', is_authenticated, name='is_authenticated'),
]
