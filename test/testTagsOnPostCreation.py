# if user makes post, check if post tags were correctly set
# TODO: implement
from django.test import TestCase, Client

from blogs.models import User, Post, Tag

class PostTestCase(TestCase):
    def test_post(self):
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

        #create post
        response = c.post('/makePost', {'postinput': 'test post', 'taginput': 'test'})
        self.assertEquals(response.status_code, 302)
        post = Post.objects.filter(content='test post').first()
        self.assertNotEquals(post, None)
        tag = Post.objects.filter(tag__name='test').first()
        self.assertEquals(tag, post)
