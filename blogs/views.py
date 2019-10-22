from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import IntegrityError
from django.urls import reverse

from .models import User, Post, Report, Tag
from .getposts import get_posts
from .deleteuser import delete_user
from .tagcode import addtag
import hashlib


class LoginView(TemplateView):
    template_name = "login/login.html"


class RegisterView(TemplateView):
    template_name = "login/register.html"

    def post(self, request):
        name = request.POST.get('nameinput', None)
        firstname, lastname = name.split()
        username = request.POST.get('usernameinput', None)
        email = request.POST.get('emailinput', None)
        password = request.POST.get('passwordinput', None)
        password_confirm = request.POST.get('confirmpasswordinput', None)
        enc_password = encrypt_string(password)

        user = User(firstname=firstname, lastname=lastname, username=username, email=email,
                    password=enc_password)

        # TODO validate all fields exist & are valid

        try:
            user.save()
        except IntegrityError:
            # TODO tell user username/email is already taken
            return redirect('register')

        request.session['userid'] = user.pk

        return redirect('mainpage')


class MainPageView(TemplateView):
    template_name = "mainpage.html"

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context


class SettingsPageView(UpdateView):
    template_name_suffix = '_update_form'
    model = User
    fields = ['firstname', 'lastname', 'username', 'email', 'password']

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.session['userid'])

    def get_context_data(self, **kwargs):
        context = super(SettingsPageView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context

    def post(self, request):
        if 'delete_user' in request.POST:
            delete_user(self.request.session.get('userid'))
            return redirect('login')
        if 'username_change' in request.POST:
            user = User.objects.get(pk=self.request.session['userid'])
            user.username = request.POST.get("username")
            user.save()
            return redirect('settingspage')
        if 'email_change' in request.POST:
            user = User.objects.get(pk=self.request.session['userid'])
            user.email = request.POST.get("email")
            user.save()
            return redirect('settingspage')
        if 'password_change' in request.POST:
            user = User.objects.get(pk=self.request.session['userid'])
            user.password = encrypt_string(request.POST.get("password"))
            user.save()
            return redirect('settingspage')
        return HttpResponse(response)


class ProfilePageView(UpdateView):
    template_name_suffix = '_profile_page'
    model = User
    fields = ['firstname', 'lastname', 'username', 'email', 'password']

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs['pk'])

    def post(self, request, pk):
        print(request.FILES)
        if 'new_bio' in request.POST:
            user = User.objects.get(id=self.request.session.get('userid'))
            user.biography = request.POST.get('new_bio', None)
            user.save()
        if 'file' in request.FILES:
            user = User.objects.get(id=self.request.session.get('userid'))
            user.profile_pic = request.POST.get('file', None)
            user.save()
            print (user.profile_pic)
        if 'updated_post' in request.POST:
            post_id = (request.POST.get('post_edit_id', None))
            post = Post.objects.get(id=post_id)
            post.content = request.POST.get('updated_post', None)
            post.save()
        if 'updated_tags' in request.POST:
            post_id = (request.POST.get('post_edit_id', None))
            post = Post.objects.get(id=post_id)
            post.content = request.POST.get('updated_post', None)
            post.save()
        if 'delete_post' in request.POST:
            post_id = request.POST.get('delete_post', None)
            post = Post.objects.get(id=post_id)
            post.delete()
        if 'like_post' in request.POST:
            post_id = request.POST.get('like_post', None)
            post = Post.objects.get(id=post_id)
        print (request.POST)

        return redirect('mainpage')

    def get_context_data(self, **kwargs):
        context = super(ProfilePageView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context


class MakePostView(TemplateView):
    template_name = "makepostpage.html"

    def get_context_data(self, **kwargs):
        context = super(MakePostView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context

    def post(self, request):
        print (request.POST)
        tags = request.POST.get('taginput', None).split(",")
        content = request.POST.get('postinput', None)
        user = User.objects.get(id=self.request.session.get('userid'))
        post = Post(content=content, creator=user)
        post.save()
        for tag in tags:
            addtag(tag, post)
        return redirect('mainpage')


class SearchView(TemplateView):
    template_name = "searchpage.html"

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context

    def post(self, request):
        user_name = request.POST.get('searchinput', None)
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return redirect('searchpage')
        return redirect(reverse('userprofilepage', kwargs={'pk': user.pk}))


class FriendView(TemplateView):
    template_name = "friend_page_profile.html"


def encrypt_string(string):
    return hashlib.sha256(string.encode()).hexdigest()


def my_authenticate(username, password):
    password = encrypt_string(password)
    query = User.objects.filter(username=username)
    if query.exists() and query[0].password == password:
        return query[0]
    else:
        return None


def login_user(request):
    username = request.POST.get('usernameinput', None)
    password = request.POST.get('passwordinput', None)
    user = my_authenticate(username, password)
    if user is not None:
        request.session['userid'] = user.pk
        return redirect('mainpage')
    else:
        # TODO: display error message to users
        return redirect('login')


def logout_user(request):
    request.session['userid'] = None
    return redirect('login')


def check_logged_in(request):
    if request.session['userid'] is None:
        return redirect('login')


##
# TODO: proper error handling:
# - User not logged in
# - User ID invalid
# - Post ID invalid
#
# TODO: implement for AJAX
#
def report_post(request, pk):
    user = User.objects.get(pk=request.session['userid'])
    post = Post.objects.get(pk=pk)
    report = Report(reporter=user, post=post)
    report.save()
    return redirect('mainpage')
