from django.conf import settings
from django.urls import path
from .views import SettingsPageView
from .views import ProfilePageView
from .views import LoginPageView, LoginDash, MainPageView, register_user
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
    path('', LoginPageView.as_view(), name='login'),
    path('loginDash', LoginDash.as_view(), name='log-in'),
    path('mainPage', MainPageView.as_view(), name='mainpage'),
<<<<<<< HEAD
    path('settingsPage', SettingsPageView.as_view(), name='settingspage'),
    path('userProfilePage', ProfilePageView.as_view(), name='userprofilepage'),
]
=======
    path('register', register_user),
]
>>>>>>> Add Basic User Registration Handling
