from django.test import TestCase
from choozen.models import Movie

class MovieTestCase(TestCase):

  DUMMY_MOVIE_TITLE = "The Matrix"
  UPDATE_MOVIE_TITLE = "The Matrix Reloaded"

  def setUp(self):
    self.movie = Movie()
    self.movie.title = self.DUMMY_MOVIE_TITLE
    self.movie.year = 1999
    self.movie.director = "Wachowski"
    self.movie.rating = 8
    self.movie.genre = "Sci-Fi"

  def test_create_movie(self):
    nb_of_movies_before = Movie.objects.count()
    new_movie = self.movie
    new_movie.save()
    nb_of_movies_after = Movie.objects.count()
    self.assertEqual(nb_of_movies_before + 1, nb_of_movies_after)
    
  def test_get_movie(self):
    new_movie = self.movie
    new_movie.save()
    movie_from_db = Movie.objects.get(title=self.DUMMY_MOVIE_TITLE)
    self.assertEqual(new_movie, movie_from_db)

  def test_update_movie(self):
    new_movie = self.movie
    new_movie.save()
    movie_from_db = Movie.objects.get(title=self.DUMMY_MOVIE_TITLE)
    movie_from_db.title = self.UPDATE_MOVIE_TITLE
    movie_from_db.save()
    self.assertEqual(movie_from_db.title, self.UPDATE_MOVIE_TITLE)

  def test_delete_movie(self):
    new_movie = self.movie
    new_movie.save()
    movie_from_db = Movie.objects.get(title=self.DUMMY_MOVIE_TITLE)
    movie_from_db.delete()
    self.assertEqual(Movie.objects.count(), 0)