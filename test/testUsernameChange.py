# if user changes username, check if it changes
# TODO: implement

# if user changes email address, check if it changes

from django.test import TestCase, Client
from blogs.models import User
from blogs.views import encrypt_string


class UserTestCase(TestCase):
    def test_change_email(self):
        name = 'Test User'
        username = 'testuser'
        email = 'test@test.com'
        password = 'test'

        username_new = 'fuck'

        c = Client()

        # create account
        response = c.post('/register',
                          {'nameinput': name, 'usernameinput': username,
                           'emailinput': email, 'passwordinput': password,
                           'confirmpasswordinput': password})

        # change email address
        response = c.post('/settingsPage',
                          {'username': username_new, 'username_change': True})

        self.assertEquals(response.status_code, 302)
        self.assertNotEquals(User.objects.get(username=username_new), None)
