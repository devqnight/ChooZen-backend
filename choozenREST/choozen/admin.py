from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
  list_display = ('title', 'year', 'genre', 'director', 'rating', 'id')
  list_filter = ('title',)
  search_fields = ('title',)
  class Meta:
    verbose_name_plural = 'Movies'
    verbose_name = 'Movie'