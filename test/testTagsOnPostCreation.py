# if user makes post, check if post tags were correctly set
# TODO: implement
from django.test import TestCase, Client

from blogs.models import User, Post, Tag, Follow

class PostTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='dummy')
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
        
        #follow
        user = User.objects.get(username=username)
        url = '/users/' + str(user.pk)
        #print(User.objects.filter(username='dummy'))
        response = c.post(url, {'followuser': 'dummy', 'followtag': 'test'}) # 'follow': 'Follow'})
        self.assertEquals(response.status_code, 302)

        #block
        dummy = User.objects.get(username='dummy')
        url = '/block/' + str(dummy.pk)
        response = c.post(url)
        self.assertEquals(response.status_code, 302)

