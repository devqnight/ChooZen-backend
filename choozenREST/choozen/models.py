from django.contrib.auth.models import Group
from django.db import models
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

class Movie(models.Model):
    title = models.CharField(max_length=50)
    year = models.IntegerField()
    director = models.CharField(max_length=50)
    rating = models.IntegerField()
    genre = models.CharField(max_length=50)
    def __str__(self):
        return self.title + " (" + str(self.year) + ")"

# Method called when a new user is created
@receiver(user_signed_up)
def new_user_signup(user, **kwargs):
    g = Group.objects.get(name='user')
    user.groups.add(g)
    user.save()