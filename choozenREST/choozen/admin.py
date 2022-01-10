from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Movie, UserProfile

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
  list_display = ('title', 'year', 'genre', 'director', 'rating', 'id')
  list_filter = ('title',)
  search_fields = ('title',)
  class Meta:
    verbose_name_plural = 'Movies'
    verbose_name = 'Movie'

class UserProfileInline(admin.StackedInline):
  model = UserProfile

class UserAdmin(UserAdmin):
  inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)