from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import User, Post

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

class ProfilePageView(TemplateView):
    template_name = "userprofilepage.html"

class MakePostView(TemplateView):
    template_name = "makepostpage.html"

    def post(self,request):
        content = request.POST.get('postinput', None)
        user = User.objects.get(id=self.request.session.get('userid'))
        post = Post(content=content, creator=user)
        post.save()


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
