# if user deletes account, check if it is deleted
# TODO: implement

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

        # change email address
        response = c.post('/settingsPage',
                          {'delete_user'})


        self.assertEquals(response.status_code, 302)
        self.assertNotEquals(User.objects.get(username=username), None)
