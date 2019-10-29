from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import IntegrityError
from django.urls import reverse

from datetime import date

from .models import User, Post, Report, Tag, Follow
from .getposts import get_posts
from .deleteuser import delete_user
from .tagcode import addtag, removetag
from .followcode import addFollow, removeFollow
from .timelinecode import timeline_by_tag, get_timeline_posts, timeline_by_text
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

    def dispatch(self, *args, **kwargs):
        if self.request.session['userid'] is None:
            return redirect('login')
        else:
            return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        context['posts'] = get_timeline_posts(User.objects.get(pk=self.request.session['userid']))
        return context



class SettingsPageView(UpdateView):
    template_name_suffix = '_update_form'
    model = User
    fields = ['firstname', 'lastname', 'username', 'email', 'password']

    def dispatch(self, *args, **kwargs):
        if self.request.session['userid'] is None:
            return redirect('login')
        else:
            return super().dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return User.objects.get(pk=self.request.session['userid'])
        except User.DoesNotExist:
            return None

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

    def dispatch(self, *args, **kwargs):
        if self.request.session['userid'] is None:
            return redirect('login')
        else:
            return super().dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs['pk'])

    def post(self, request, pk):
        print(request.POST)
        if 'new_bio' in request.POST:
            user = User.objects.get(id=self.request.session.get('userid'))
            user.biography = request.POST.get('new_bio', None)
            user.save()
        if 'file' in request.FILES:
            user = User.objects.get(id=self.request.session.get('userid'))
            user.profile_pic = request.FILES.get('file', None)
            user.save()
            print (user.profile_pic)
        if 'updated_post' in request.POST:
            post_id = (request.POST.get('post_edit_id', None))
            post = Post.objects.get(id=post_id)
            post.content = request.POST.get('updated_post', None)
            post.save()
        if 'edit_tags' in request.POST:
            post_id = (request.POST.get('tags_edit_id', None))
            post = Post.objects.get(id=post_id)
            name = request.POST.get('edit_tags', None)
            if not post.tag_set.filter(name=name).exists():
                addtag(name,post)
            else:
                removetag(name, post)
        if 'delete_post' in request.POST:
            post_id = request.POST.get('delete_post', None)
            post = Post.objects.get(id=post_id)
            post.delete()
        if 'like_post' in request.POST:
            post_id = request.POST.get('like_post', None)
            post = Post.objects.get(id=post_id)
            user = User.objects.get(id=self.request.session.get('userid'))
            post.likers.add(user)
            print(post.likers.all().count())
        if 'followuser' in request.POST:
            follower_id = self.request.session.get('userid')
            following_name = request.POST.get('followuser')
            tag_name = request.POST.get('followtag')
            if request.POST.get('Following') is '1':
                addFollow(follower_id, following_name, tag_name)
            else:
                removeFollow(follower_id, following_name, tag_name)
            follower = follower = User.objects.get(id=follower_id)
            follow_list = Follow.objects.filter(follower=follower)
            for follow in follow_list:
                print (follow.following.username)
                for tag in follow.tags.all():
                    print (tag.name)
        return redirect('mainpage')

    def get_context_data(self, **kwargs):
        context = super(ProfilePageView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context

class BannedView(TemplateView):
    template_name = "banned.html"

class MakePostView(TemplateView):
    template_name = "makepostpage.html"

    def dispatch(self, *args, **kwargs):
        if self.request.session['userid'] is None:
            return redirect('login')
        else:
            return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MakePostView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context

    def post(self, request):
        tags = request.POST.get('taginput', None).split(",")
        content = request.POST.get('postinput', None)
        image = request.FILES.get('image', None)
        user = User.objects.get(id=self.request.session.get('userid'))
        if not content and not image:
            # TODO: report error
            return redirect('mainpage')
        post = Post(content=content, creator=user, image=image)
        post.save()
        for tag in tags:
            addtag(tag, post)
        return redirect('mainpage')

class SearchView(TemplateView):
    template_name = "searchpage.html"

    def dispatch(self, *args, **kwargs):
        if self.request.session['userid'] is None:
            return redirect('login')
        else:
            return super().dispatch(*args, **kwargs)

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

class UserSearchView(TemplateView):
    template_name = "user_search_page.html"

class UserSearchResultView(ListView):
    template_name = "user_search_result_page.html"
    model = Post

    def get_queryset(self, **kwargs):
        if 'word_search' in self.request.GET:
            post_content = self.request.GET.get('word_search')
            return Post.objects.filter(content__icontains=post_content)

        if 'tag_search' in self.request.GET:
            post_tag = self.request.GET.get('tag_search')
            return Post.objects.filter(tag__name=post_tag)
        
        if 'user_search' in self.request.GET:
            post_user = self.request.GET.get('user_search')
            user_id = User.objects.get(username=post_user).id
            return Post.objects.filter(creator=user_id)

        if 'tag_user_search' in self.request.GET:
            post_combo = self.request.GET.get('tag_user_search')
            split_combo = post_combo.split('/')
            user_id = User.objects.get(username=split_combo[1]).id
            return Post.objects.filter(tag__name=split_combo[0],creator=user_id) 
        
        if 'date_search' in self.request.GET:
            given = self.request.GET.get('date_search')
            date_array = given.split('/')
            date = date_array[2] + "-" + date_array[0] + "-" + date_array[1]
            return Post.objects.filter(created=date)

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
        if user.banned_until is not None and user.banned_until > date.today():
            return redirect('banned')
        request.session['userid'] = user.pk
        return redirect('mainpage')
    else:
        # TODO: display error message to users
        return redirect('login')


def logout_user(request):
    request.session['userid'] = None
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
