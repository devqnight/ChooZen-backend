from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from choozen.models import User
# python manage.py test
class UserTestCase(TestCase):

    DUMMY_USER_NAME = "John"
    DUMMY_USER_FIRSTNAME = "John"
    DUMMY_USER_LASTNAME = "Doe"
    DUMMY_USER_EMAIL = "testuser@testage.com"
    DUMMY_USER_PASSWORD = "testpassword"
    DUMMY_USER_BIRTHDATE = "1999-01-01"

    DUMMY_USER2_NAME = "randomname"
    DUMMY_USER2_EMAIL = "random@email.com"
    DUMMY_USER2_PASSWORD = "randompswd"
    DUMMY_USER2_BIRTHDATE = "2012-12-12"
  
    def setUp(self):
      self.user = User()
      self.user.username = self.DUMMY_USER_NAME
      self.user.first_name = self.DUMMY_USER_FIRSTNAME
      self.user.last_name = self.DUMMY_USER_LASTNAME
      self.user.email = self.DUMMY_USER_EMAIL
      self.user.password = self.DUMMY_USER_PASSWORD
      self.user.birthdate = self.DUMMY_USER_BIRTHDATE
      self.user2 = User()
      self.user2.username = self.DUMMY_USER2_NAME
      self.user2.email = self.DUMMY_USER2_EMAIL
      self.user2.password = self.DUMMY_USER2_PASSWORD
      self.user2.birthdate = self.DUMMY_USER2_BIRTHDATE

    def test_create_user(self):
      nb_of_users_before = User.objects.count()
      new_user = self.user
      new_user.save()
      nb_of_users_after = User.objects.count()
      self.assertEqual(nb_of_users_before + 1, nb_of_users_after)

    def test_create_user_firstname(self):
      new_user = self.user
      new_user.save()
      user_from_db = User.objects.get(first_name=self.user.first_name)
      self.assertEqual(new_user.first_name, user_from_db.first_name)

    def test_create_user_with_same_name(self):
      new_user = self.user
      new_user.save()
      new_user2 = self.user2
      new_user2.username = self.user.username
      with self.assertRaises(IntegrityError):
        new_user2.save()

    def test_create_user_with_same_email(self):
      new_user = self.user
      new_user.save()
      new_user2 = self.user2
      new_user2.email = self.user.email
      with self.assertRaises(IntegrityError):
        new_user2.save()

    def test_create_user_with_missing_name(self):
      new_user = self.user
      new_user.username = None
      with self.assertRaises(IntegrityError):
        new_user.save()
      
    def test_create_user_date_error(self):
      new_user = self.user
      new_user.birthdate = "1999-01-32"
      with self.assertRaises(ValidationError):
        new_user.save()

    def test_case_user_date_missing(self):
      new_user = self.user
      new_user.birthdate = ""
      with self.assertRaises(ValidationError):
        new_user.save()

    def test_get_user(self):
      new_user = self.user
      new_user.save()
      user_from_db = User.objects.get(username=self.user.username)
      self.assertEqual(new_user, user_from_db)

    def test_get_user_with_wrong_name(self):
      new_user = self.user
      new_user.save()
      with self.assertRaises(User.DoesNotExist):
        User.objects.get(username="wrongname")

    def test_get_user_with_wrong_email(self):
      new_user = self.user
      new_user.save()
      with self.assertRaises(User.DoesNotExist):
        User.objects.get(email="wrongemail")

    def test_update_user(self):
      new_user = self.user
      new_user.save()
      user_from_db = User.objects.get(username=self.user.username)
      user_from_db.username = self.user2.username
      user_from_db.save()
      self.assertEqual(user_from_db.username, self.user2.username)

    def test_update_user_with_same_name(self):
      new_user = self.user
      new_user.save()
      new_user2 = self.user2
      new_user2.save()
      user_from_db = User.objects.get(username=self.user2.username)
      user_from_db.username = self.user.username
      with self.assertRaises(IntegrityError):
        user_from_db.save()

    def test_update_user_with_same_email(self):
      new_user = self.user
      new_user.save()
      new_user2 = self.user2
      new_user2.save()
      user_from_db = User.objects.get(username=self.user2.username)
      user_from_db.email = self.user.email
      with self.assertRaises(IntegrityError):
        user_from_db.save()

    def test_delete_user(self):
      new_user = self.user
      new_user.save()
      user_from_db = User.objects.get(username=self.user.username)
      user_from_db.delete()
      self.assertEqual(User.objects.count(), 0)

    def test_delete_user_with_wrong_name(self):
      new_user = self.user
      new_user.save()
      with self.assertRaises(User.DoesNotExist):
        User.objects.get(username="wrongname").delete()
