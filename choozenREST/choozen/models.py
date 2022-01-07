from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=50)
    year = models.IntegerField()
    director = models.CharField(max_length=50)
    rating = models.IntegerField()
    genre = models.CharField(max_length=50)
    def __str__(self):
        return self.title + " (" + str(self.year) + ")"