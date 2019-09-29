from django.views.generic.base import TemplateView

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
