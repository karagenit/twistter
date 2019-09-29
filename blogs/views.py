from django.views.generic.base import TemplateView

class LoginRealPageView(TemplateView):
    template_name = "loginReal.html"

class LoginPageView(TemplateView):
    template_name = "login.html"
