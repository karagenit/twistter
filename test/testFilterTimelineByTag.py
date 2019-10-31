# if user changes email address, check if it changes

from django.test import TestCase, Client
from blogs.models import User
from blogs.views import encrypt_string


class UserTestCase(TestCase):
    def test_filter_timeline_by_word_search(self):
        c = Client()
        name = 'test user'
        username = 'testuser'
        email = 'test@test.com'
        password = 'test'

        #create account
        response = c.post('/register',
                          {'nameinput': name, 'usernameinput': username,
                           'emailinput': email, 'passwordinput': password,
                           'confirmpasswordinput': password})

        #create post 1
        response = c.post('/makePost', {'postinput': 'Black', 'taginput': 'test'})
        post = Post.objects.filter(content='test post').first()
        tag = Post.objects.filter(tag__name='test').first()

        #create post 2
        response = c.post('/makePost', {'postinput': 'Blue', 'taginput': 'test'})
        post = Post.objects.filter(content='test post').first()
        tag = Post.objects.filter(tag__name='test').first()

        # create post 3
        response = c.post('/makePost', {'postinput': 'Red', 'taginput': 'test'})
        post = Post.objects.filter(content='test post').first()
        tag = Post.objects.filter(tag__name='test').first()

        # filter
        response = c.post('/mainPage', {'tag_search': 'test'})
        self.assertEquals(response.status_code, 302)
