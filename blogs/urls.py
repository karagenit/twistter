from django.conf import settings
from django.urls import path
from .views import LoginPageView
from .views import LoginDash
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
    path('', LoginPageView.as_view(), name='login'),
    path('loginDash', LoginDash.as_view(), name='log-in'),
]