from django.conf import settings
from django.urls import path
from .views import LoginPageView
from .views import LoginDash
from .views import MainPageView
from .views import SettingsPageView
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
    path('', LoginPageView.as_view(), name='login'),
    path('loginDash', LoginDash.as_view(), name='log-in'),
    path('mainPage', MainPageView.as_view(), name='mainpage'),
    path('settingsPage', SettingsPageView.as_view(), name='settingspage'),
]