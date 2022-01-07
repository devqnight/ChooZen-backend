from django.db import models
from django.contrib.auth.models import AbstractUser

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.username

class Users(AbstractUser):
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICES = (
      (CREATOR, 'Créateur'),
      (SUBSCRIBER, 'Abonné'),
    )
    profile_photo = models.ImageField(verbose_name='Photo de profil')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')

class Movie(models.Model):
    title = models.CharField(max_length=50)
    year = models.IntegerField()
    director = models.CharField(max_length=50)
    rating = models.IntegerField()
    genre = models.CharField(max_length=50)
    def __str__(self):
        return self.title + " (" + str(self.year) + ")"