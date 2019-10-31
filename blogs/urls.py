from django.conf import settings
from django.urls import path
from .views import RegisterView, LoginView, MainPageView, ProfilePageView, SettingsPageView, login_user, MakePostView, SearchView, logout_user, FriendView, report_post, BannedView, UserSearchView, UserSearchResultView, block_user, unblock_user
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
    path('register', RegisterView.as_view(), name='register'),
    path('', LoginView.as_view(), name='login'),
    path('mainPage', MainPageView.as_view(), name='mainpage'),
    path('settingsPage', SettingsPageView.as_view(), name='settingspage'),
    path('users/settingsPage', SettingsPageView.as_view(), name='settingspage'),
    path('makePost', MakePostView.as_view(), name='makepostpage'),
    path('users/<int:pk>', ProfilePageView.as_view(), name='userprofilepage'),
    path('login', login_user),
    path('post', MakePostView.as_view(), name='makepostpage'),
    path('search', SearchView.as_view(), name='searchpage'),
    path('logout', logout_user),
    path('friend', FriendView.as_view(), name='friend_page'),
    path('report/<int:pk>', report_post, name='report'),
    path('banned', BannedView.as_view(), name='banned'),
    path('search_page', UserSearchView.as_view(), name='search_page'),
    path('search/results', UserSearchResultView.as_view(), name='search_results'),
    path('block/<int:pk>', block_user, name='block'),
    path('unblock/<int:pk>', unblock_user, name='unblock'),
]
