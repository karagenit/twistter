from django.test import TestCase, Client
from django.db import IntegrityError

from blogs.models import User
from blogs.views import encrypt_string

class UserTestCase(TestCase):
    def test_create_user(self):
        firstname = 'Test'
        lastname = 'User'
        username = 'testuser'
        email = 'test@test.com'
        password = encrypt_string('test')

        User.objects.create(firstname=firstname, lastname=lastname,
                            username=username, email=email, password=password)

        user = User.objects.get(username=username)

        self.assertNotEqual(user, None)
        self.assertEqual(user.firstname, firstname)
        self.assertEqual(user.lastname, lastname)
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.password, password)

    def test_non_user(self):
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='doesnotexist')

    def test_duplicate_user(self):
        firstname = 'Test'
        lastname = 'User'
        username = 'testuser'
        email = 'test@test.com'
        password = encrypt_string('test')

        User.objects.create(firstname=firstname, lastname=lastname,
                            username=username, email=email, password=password)

        with self.assertRaises(IntegrityError):
            User.objects.create(firstname='other', lastname='user',
                                username=username, email='none@none.com',
                                password=password)

