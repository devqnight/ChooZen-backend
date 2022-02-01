from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Movie, User

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
  list_display = ('title', 'release_date', 'imdb_rating', 'imdb_id')
  list_filter = ('title',)
  search_fields = ('title',)
  class Meta:
    verbose_name_plural = 'Movies'
    verbose_name = 'Movie'

@admin.register(User)
class UserAdmin(UserAdmin):
  list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'birthdate')
  list_filter = ('username',)
  search_fields = ('username',)
  class Meta:
    verbose_name_plural = 'Users'
    verbose_name = 'User'