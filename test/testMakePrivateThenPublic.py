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

        email_new = 'new@new.com'

        c = Client()

        # create account
        response = c.post('/register',
                          {'nameinput': name, 'usernameinput': username,
                           'emailinput': email, 'passwordinput': password,
                           'confirmpasswordinput': password})


        # set privacy to true
        response = c.post('/settingspage',
                          {'private_change': true})

        # set privacy to false
        response = c.post('/settingspage',
                          {'private_change': true})

        self.assertequals(response.status_code, 302)
        self.assertnotequals(user.objects.get(username=username).private, true)
