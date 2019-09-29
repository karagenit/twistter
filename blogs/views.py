from django.views.generic.base import TemplateView
from django.http import HttpResponse

class LoginDash(TemplateView):
    template_name = "log-in.html"

class LoginPageView(TemplateView):
    template_name = "login.html"

class MainPageView(TemplateView):
    template_name = "mainpage.html"

class SettingsPageView(TemplateView):
    template_name = "settingspage.html"

class ProfilePageView(TemplateView):
    template_name = "userprofilepage.html"

def register_user(request):
    # TODO register user

    # TODO redirect to user's homepage
    return HttpResponse("User Registered!")
