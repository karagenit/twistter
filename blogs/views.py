from django.views.generic.base import TemplateView

class LoginPageView(TemplateView):
    template_name = "login.html"
