from django.views.generic.base import TemplateView

class LoginDash(TemplateView):
    template_name = "log-in.html"

class LoginPageView(TemplateView):
    template_name = "login.html"
