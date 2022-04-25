from random import choice
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

class Movie(models.Model):
    imdb_id = models.CharField(max_length=10, unique=True, primary_key=True, null=False, blank=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    length = models.DurationField(null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    content_rating = models.CharField(max_length=20, null=True, blank=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    #directors = models.ManyToManyField('Person', related_name='directed', blank=True)
    # TODO see example below
    #genres = models.ManyToManyField('Genre', related_name='movies', blank=True)
    def __str__(self):
        return self.title + " (" + str(self.release_date) + ")"

# Example from django doc 
# https://docs.djangoproject.com/fr/4.0/ref/models/fields/#manytomanyfield

class Person(models.Model):
    imdb_id = models.CharField(max_length=10, unique=True, primary_key=True, null=False, blank=False)
    full_name = models.CharField(max_length=50)
    picture_url = models.URLField(null=True, blank=True)

class Genre(models.Model):
    type = models.CharField(max_length=50)

class HasGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'genre')

class Directed(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    director = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'director')

class Played(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Person, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('movie', 'actor')

class User(AbstractUser):
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True, blank=True)

class MemberLevel(models.Model):
    number_members_per_group = models.IntegerField(default=5)

class GroupList(models.Model):
    title = models.CharField(max_length=50)
    member_level = models.OneToOneField(MemberLevel, on_delete=models.CASCADE)


# Method called when a new user is created
@receiver(user_signed_up)
def new_user_signup(user, **kwargs):
    g = Group.objects.get(name='user')
    user.groups.add(g)
    user.save()