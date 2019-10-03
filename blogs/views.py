from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.shortcuts import redirect
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

        user.save()

        # TODO validate all fields exist & are valid

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



class MakePostView(TemplateView):
    template_name = "makepostpage.html"

    def post(self,request):
        content = request.POST.get('postinput', None)
        user = User.objects.get(id=self.request.session.get('userid'))
        post = Post(content=content, creator=user)
        post.save()
        return redirect('mainpage')

class SearchView(TemplateView):
    template_name = "searchpage.html"

    def post(self,request):
        user_name = request.POST.get('searchinput', None)
        user = User.objects.get(username=user_name)
        fn = user.firstname
        ln = user.lastname
        em = user.email
        id = user.id
        posts = get_posts(id)
        posts.append(user_name)
        posts.append(' ')
        posts.append(fn)
        posts.append(' ')
        posts.append(ln)
        posts.append(' ')
        posts.append(em)
        return HttpResponse(posts)


def encrypt_string(string):
    return hashlib.sha256(string.encode()).hexdigest()

def my_authenticate(username, password):
    password = encrypt_string(password)
    user = User.objects.get(username=username)
    if user.password == password:
        return user
    else:
        return None

def login_user(request):
    print("Logging in...")
    username = request.POST.get('usernameinput', None)
    password = request.POST.get('passwordinput', None)
    user = my_authenticate(username, password)
    if user is not None:
        print("Success")
        request.session['userid'] = user.pk
        return redirect('mainpage')
    else:
        print("Failure")
        return redirect('login')
