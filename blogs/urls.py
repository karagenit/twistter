from django.conf import settings
from django.urls import path
from .views import RegisterView, LoginView, MainPageView, ProfilePageView, SettingsPageView, login_user, MakePostView
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
    path('register', RegisterView.as_view(), name='register'),
    path('', LoginView.as_view(), name='login'),
    path('mainPage', MainPageView.as_view(), name='mainpage'),
    path('settingsPage', SettingsPageView.as_view(), name='settingspage'),
    path('users/<int:pk>', ProfilePageView.as_view(), name='userprofilepage'),
    path('login', login_user),
    path('post', MakePostView.as_view(), name='makepostpage')
]
