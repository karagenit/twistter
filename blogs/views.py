from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import User

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

        return redirect('mainpage')

class MainPageView(TemplateView):
    template_name = "mainpage.html"

class SettingsPageView(TemplateView):
    template_name = "settingspage.html"

class ProfilePageView(TemplateView):
    template_name = "userprofilepage.html"

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
