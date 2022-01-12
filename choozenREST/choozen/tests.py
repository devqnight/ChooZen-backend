from django.test import TestCase

from choozen.models import Movie, User

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

class UserTestCase(TestCase):

    DUMMY_USER_NAME = "John"
    UPDATE_USER_NAME = "Quentin"
  
    def setUp(self):
      self.user = User()
      self.user.username = self.DUMMY_USER_NAME
      self.user.email = "testuser@testage.com"
      self.user.password = "testpassword"
      self.user.birthdate = "1999-01-01"

    def test_create_user(self):
      nb_of_users_before = User.objects.count()
      new_user = self.user
      new_user.save()
      nb_of_users_after = User.objects.count()
      self.assertEqual(nb_of_users_before + 1, nb_of_users_after)

    def test_get_user(self):
      new_user = self.user
      new_user.save()
      user_from_db = User.objects.get(username=self.DUMMY_USER_NAME)
      self.assertEqual(new_user, user_from_db)

    def test_update_user(self):
      new_user = self.user
      new_user.save()
      user_from_db = User.objects.get(username=self.DUMMY_USER_NAME)
      user_from_db.username = self.UPDATE_USER_NAME
      user_from_db.save()
      self.assertEqual(user_from_db.username, self.UPDATE_USER_NAME)

    def test_delete_user(self):
      new_user = self.user
      new_user.save()
      user_from_db = User.objects.get(username=self.DUMMY_USER_NAME)
      user_from_db.delete()
      self.assertEqual(User.objects.count(), 0)
