from django.test import TestCase, Client

from blogs.models import User

from blogs.views import encrypt_string

class UserTestCase(TestCase):
    def test_register_user(self):
        name = 'Test User'
        username = 'testuser'
        email = 'test@test.com'
        password = 'test'

        c = Client()
        response = c.post('/register',
                          {'nameinput': name, 'usernameinput': username,
                           'emailinput': email, 'passwordinput': password,
                           'confirmpasswordinput': password})
        
        self.assertEquals(response.status_code, 302)
        self.assertNotEquals(User.objects.get(username=username), None)
