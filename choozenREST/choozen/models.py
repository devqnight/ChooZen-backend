from random import choice
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
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
    year = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    runtimeStr = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.title + " (" + str(self.release_date) + ")"

# Example from django doc 
# https://docs.djangoproject.com/fr/4.0/ref/models/fields/#manytomanyfield

class MemberLevel(models.Model):
    number_members_per_group = models.IntegerField(null=False, blank=False)

class GroupLevel(models.Model):
    number_of_groups = models.IntegerField(null=False, blank=False)

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
    group_level = models.ForeignKey(GroupLevel, on_delete=models.CASCADE, default=1)

class GroupList(models.Model):
    title = models.CharField(max_length=50)
    member_level = models.ForeignKey(MemberLevel, on_delete=models.CASCADE, default=1)

class IsFriendWith(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')

    class Meta:
        unique_together = ('user1', 'user2')

class IsPartOf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupList, on_delete=models.CASCADE)
    is_creator = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'group')

class HasReviewed(models.Model):
    partOf = models.ForeignKey(IsPartOf, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    note = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(4)])

    class Meta:
        unique_together = ('partOf', 'movie')

class HasProposed(models.Model):
    partOf = models.ForeignKey(IsPartOf, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comments = models.TextField(null=True, blank=True)
    is_watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ('partOf', 'movie')

# python manage.py makemigrations
# Method called when a new user is created
@receiver(user_signed_up)
def new_user_signup(user, **kwargs):
    g = Group.objects.get(name='user')
    user.groups.add(g)
    user.save()