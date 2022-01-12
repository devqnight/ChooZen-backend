from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

class Movie(models.Model):
    imdb_id = models.CharField(max_length=10, unique=True, primary_key=True)
    title = models.CharField(max_length=50)
    length = models.TimeField(null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    content_rating = models.CharField(max_length=10, null=True, blank=True)
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
# class Person(models.Model):
#     name = models.CharField(max_length=50)
# 
# class Group(models.Model):
#     name = models.CharField(max_length=128)
#     members = models.ManyToManyField(
#         Person,
#         through='Membership',
#         through_fields=('group', 'person'),
#     )
# 
# class Membership(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     person = models.ForeignKey(Person, on_delete=models.CASCADE)
#     inviter = models.ForeignKey(
#         Person,
#         on_delete=models.CASCADE,
#         related_name="membership_invites",
#     )
#     invite_reason = models.CharField(max_length=64)

class User(AbstractUser):
    birthdate = models.DateField(null=True, blank=True)

# Method called when a new user is created
@receiver(user_signed_up)
def new_user_signup(user, **kwargs):
    g = Group.objects.get(name='user')
    user.groups.add(g)
    user.save()