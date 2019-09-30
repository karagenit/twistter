from django.test import TestCase, Client

from blogs.models import User

from blogs.views import encrypt_string

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(firstname='Test', lastname='User', username='testuser',
                            email='test@test.com', password=encrypt_string('test'))

    def test_login(self):
        c = Client()
        response = c.post('/login', {'usernameinput': 'testuser', 'passwordinput': 'test'})
        self.assertEquals(response.status_code, 302)
