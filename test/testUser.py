from django.test import TestCase

from blogs.models import User

from blogs.views import encrypt_string

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(firstname='Test', lastname='User', username='testuser',
                            email='test@test.com', password=encrypt_string('test'))

    def test_user_exists(self):
        self.assertNotEqual(User.objects.get(username='testuser'), None)
