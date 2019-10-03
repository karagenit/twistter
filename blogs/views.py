from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import IntegrityError

from .models import User, Post
from .getposts import get_posts
from .deleteuser import delete_user

import hashlib

class LoginView(TemplateView):
    template_name = "login/login.html"

class RegisterView(TemplateView):
    template_name = "login/register.html"

    def post(self, request):
        name = request.POST.get('nameinput', None)
        firstname, lastname = name.split()
        username = request.POST.get('usernameinput', None)
        email = request.POST.get('emailinput', None)
        password = request.POST.get('passwordinput', None)
        password_confirm = request.POST.get('confirmpasswordinput', None)
        enc_password = encrypt_string(password)

        user = User(firstname=firstname, lastname=lastname, username=username, email=email,
                    password=enc_password)

        # TODO validate all fields exist & are valid

        try:
            user.save()
        except IntegrityError:
            # TODO tell user username/email is already taken
            return redirect('register')

        request.session['userid'] = user.pk

        return redirect('mainpage')

class MainPageView(TemplateView):
    template_name = "mainpage.html"

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context

class SettingsPageView(UpdateView):
    template_name_suffix = '_update_form'
    model = User
    fields = ['firstname', 'lastname', 'username', 'email', 'password']

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.session['userid'])

    def get_context_data(self, **kwargs):
        context = super(SettingsPageView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context

    def post(self,request):
        if 'delete_user' in request.POST:
            delete_user(self.request.session.get('userid'))
            return redirect('login')
        if 'username_change' in request.POST:
            user = User.objects.get(pk=self.request.session['userid'])
            user.username = request.POST.get("username")
            user.save()
            return redirect('settingspage')
        if 'email_change' in request.POST:
            user = User.objects.get(pk=self.request.session['userid'])
            user.email = request.POST.get("email")
            user.save()
            return redirect('settingspage')
        if 'password_change' in request.POST:
            user = User.objects.get(pk=self.request.session['userid'])
            user.password = encrypt_string(request.POST.get("password"))
            user.save()
            return redirect('settingspage')
        return HttpResponse(response)

class ProfilePageView(UpdateView):
    template_name_suffix = '_profile_page'
    model = User
    fields = ['firstname', 'lastname', 'username', 'email', 'password']

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.session['userid'])


    def post(self,request,pk):
        print(request.FILES)
        if 'new_bio' in request.POST:
            user = User.objects.get(id=self.request.session.get('userid'))
            user.biography = request.POST.get('new_bio', None)
            user.save()
        if 'file' in request.FILES:
            user = User.objects.get(id=self.request.session.get('userid'))
            user.profile_pic = request.FILES.get('file', None)
            user.save()
            print (user.profile_pic)
        return redirect('mainpage')

    def get_context_data(self, **kwargs):
        context = super(ProfilePageView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context



class MakePostView(TemplateView):
    template_name = "makepostpage.html"

    def get_context_data(self, **kwargs):
        context = super(MakePostView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context

    def post(self,request):
        content = request.POST.get('postinput', None)
        user = User.objects.get(id=self.request.session.get('userid'))
        post = Post(content=content, creator=user)
        post.save()
        return redirect('mainpage')

class SearchView(TemplateView):
    template_name = "searchpage.html"

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context

    def post(self,request):
        user_name = request.POST.get('searchinput', None)
        user = User.objects.get(username=user_name)
        #fn = user.firstname
        #ln = user.lastname
        #em = user.email
        #id = user.id
        #posts = get_posts(id)
        #posts.append(user_name)
        #posts.append(' ')
        #posts.append(fn)
        #posts.append(' ')
        #posts.append(ln)
        #posts.append(' ')
        #posts.append(em)
        return redirect('friend_page')

class FriendView(TemplateView):
    template_name = "friend_page_profile.html"

def encrypt_string(string):
    return hashlib.sha256(string.encode()).hexdigest()

def my_authenticate(username, password):
    password = encrypt_string(password)
    query = User.objects.filter(username=username)
    if query.exists() and query[0].password == password:
        return query[0]
    else:
        return None

def login_user(request):
    username = request.POST.get('usernameinput', None)
    password = request.POST.get('passwordinput', None)
    user = my_authenticate(username, password)
    if user is not None:
        request.session['userid'] = user.pk
        return redirect('mainpage')
    else:
        # TODO: display error message to users
        return redirect('login')

def logout_user(request):
    request.session['userid'] = None
    return redirect('login')
