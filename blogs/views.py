from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db import IntegrityError
from django.urls import reverse
from django.db.models import Count, Q
from django.utils import timezone
import datetime
import pytz
from django.db.models import Count
from operator import attrgetter

from .models import User, Post, Report, Tag, Follow, Chat, Message, Comment
from .commentcode import add_comment
from .getposts import get_posts
from .deleteuser import delete_user
from .tagcode import addtag, removetag
from .followcode import addFollow, removeFollow, getFollowers, getFollowing, deleteFollow
from .timelinecode import timeline_by_tag, get_timeline_posts, timeline_by_text, timeline_by_date, timeline_by_trending
from .postrequestcode import post_request_from_post
from .chatcode import createChat, addUser, removeUser, createMessage, deleteMessage, getChats, deleteChat

import hashlib
import pyotp

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
        user = User.objects.get(pk=self.request.session['userid'])
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        context['user'] = user
        context['follows'] = getFollowing(self.request.session['userid'])
        if 'word_search' in self.request.GET:
            word = self.request.GET.get('word_search',None)
            context['posts'] = timeline_by_text(user,word)
        elif 'date_search' in self.request.GET:
            date = self.request.GET.get('date_search',None)
            #date_array = given.split('/')
            #date = date_array[2] + "-" + date_array[0] + "-" + date_array[1]
            context['posts'] = timeline_by_date(user,date)
        elif 'tag_search' in self.request.GET:
            tag_name = self.request.GET.get('tag_search',None)
            print('context 3')
            print(tag_name)
            context['posts'] = timeline_by_tag(user,tag_name)
        elif 'trending' in self.request.GET:
            print('context 4')
            context['posts'] = timeline_by_trending(user)
        else:
            print('context 5')
            context['posts'] = get_timeline_posts(user)
        user.prev_time_line_view = user.curr_time_line_view
        user.curr_time_line_view = timezone.now()
        user.save()
        return context

    def post(self,request):
        print(request)
        post_request_from_post(self,request)
        return redirect('mainpage')



class SettingsPageView(UpdateView):
    template_name_suffix = '_update_form'
    model = User
    fields = ['firstname', 'lastname', 'username', 'email', 'password', 'private']

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
        print(request.POST)
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
        if 'private_change' in request.POST:
            user = User.objects.get(pk=self.request.session['userid'])
            user.private = 'private' in request.POST
            user.save()
            return redirect('settingspage')
        if 'chat_privacy' in request.POST:
            user = User.objects.get(pk=self.request.session['userid'])
            user.chat_privacy = request.POST.get("chat_privacy")
            user.save()
        return redirect('settingspage')


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
        post_request_from_post(self, request)
        return redirect(reverse('userprofilepage', kwargs={'pk': self.kwargs['pk']}))

    def get_context_data(self, **kwargs):
        context = super(ProfilePageView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        context['following_list'] = getFollowing(context['user'].id)
        context['follower_list'] = getFollowers(context['user'].id)
        context['logged_in_user'] = User.objects.get(id=self.request.session.get('userid', None))
        context['follows_me'] = context['user'].followings.filter(following__id = context['userid']).exists()
        return context

class BannedView(TemplateView):
    template_name = "banned.html"

class ChatView(TemplateView):
    template_name = "chatpage.html"

    def dispatch(self, *args, **kwargs):
        if self.request.session['userid'] is None:
            return redirect('login')
        else:
            return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        context['chat'] = Chat.objects.get(id=self.kwargs['pk'])
        context['all_chats'] = getChats(self.request.session.get('userid', None))
        return context

    def post(self, request, pk):
        print(request.POST)
        if 'add_member' in request.POST:
            try:
                user_id = User.objects.get(username=request.POST.get('add_member', None)).id
                addUser(pk,user_id)
            except:
                print("Invalid User Request")
        if 'remove_member' in request.POST:
            try:
                user_id = User.objects.get(username=request.POST.get('remove_member', None)).id
                user = self.request.session.get('userid', None)
                if user_id != user:
                        removeUser(pk,user_id)
            except:
                print("Invalid User Request")
        if 'delete_chat' in request.POST:
            user = self.request.session.get('userid', None)
            deleteChat(pk, user)
            return redirect('chatnavpage')
        if 'leave_chat' in request.POST:
            user = self.request.session.get('userid', None)
            removeUser(pk, user)
            return redirect('chatnavpage')
        if 'delete_message' in request.POST:
            message_id = request.POST.get('delete_message', None)
            deleteMessage(message_id)
        if 'postinput' in request.POST:
            user_id = self.request.session.get('userid', None)
            content = username=request.POST.get('postinput', None)
            image = request.FILES.get('image', None)
            print(request.FILES)
            if len(content) != 0:
                createMessage(user_id, content, pk, image)
        return redirect('chatviewpage', pk=pk)

class ChatNavView(TemplateView):
    template_name = "chatnav.html"

    def dispatch(self, *args, **kwargs):
        if self.request.session['userid'] is None:
            return redirect('login')
        else:
            return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        context['all_chats'] = getChats(self.request.session.get('userid', None))
        return context

    def post(self, request):
        if 'create_chat' in request.POST:
            name = request.POST.get('create_chat', None)
            chat = createChat(name, self.request.session.get('userid', None))
            return redirect('chatviewpage', pk=chat.id)

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
        private = 'private' in request.POST
        if not content and not image:
            # TODO: report error
            return redirect('mainpage')
        post = Post(content=content, creator=user, image=image, private=private)
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

    def dispatch(self, *args, **kwargs):
        if self.request.session['userid'] is None:
            return redirect('login')
        else:
            return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context

class UserSearchResultView(ListView):
    template_name = "user_search_result_page.html"
    model = Post

    def dispatch(self, *args, **kwargs):
        if self.request.session['userid'] is None:
            return redirect('login')
        else:
            return super().dispatch(*args, **kwargs)

    def get_queryset(self, **kwargs):
        if 'word_search' in self.request.GET:
            post_content = self.request.GET.get('word_search')
            return Post.objects.filter(content__icontains=post_content)

        if 'tag_search' in self.request.GET:
            post_tag = self.request.GET.get('tag_search')
            return Post.objects.filter(tag__name=post_tag)

        if 'user_search' in self.request.GET:
            post_user = self.request.GET.get('user_search')
            try:
                user_id = User.objects.get(username=post_user).id
            except:
                return None
            return Post.objects.filter(creator=user_id)

        if 'name_search' in self.request.GET:
            post_user = self.request.GET.get('name_search')
            name = post_user.split(" ")
            if len(name) is 1:
                return Post.objects.filter(Q(creator__firstname__icontains=name[0]) | Q(creator__lastname__icontains=name[0]))
            else:
                return Post.objects.filter(Q(creator__firstname__icontains=name[0]) | Q(creator__lastname__icontains=name[0]) | Q(creator__firstname__icontains=name[1]) | Q(creator__lastname__icontains=name[1]))

        if 'tag_user_search' in self.request.GET:
            post_combo = self.request.GET.get('tag_user_search')
            split_combo = post_combo.split('/')
            try:
                user_id = User.objects.get(username=split_combo[1]).id
                return Post.objects.filter(tag__name=split_combo[0],creator=user_id)
            except:
                return None
        if 'date_search' in self.request.GET:
            given = self.request.GET.get('date_search')
            date_array = given.split('/')
            #date = date_array[2] + "-" + date_array[0] + "-" + date_array[1]
            try:
                return Post.objects.filter(created__contains=datetime.date(int(date_array[2]), int(date_array[0]), int(date_array[1])))
            except:
                return None
                
        if 'top_tag_search' in self.request.GET:
            tag = self.request.GET.get('top_tag_search')
            top_posts = Post.objects.filter(tag__name=tag).annotate(t_count=Count('likers')).order_by('-t_count')
            return top_posts

        if 'trending' in self.request.GET:
            return Post.objects.all().annotate(num_likes=Count('likers')).order_by('-num_likes')

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['userid'] = self.request.session.get('userid', None)
        return context


    def post(self, request):
        post_request_from_post(self, request)
        return redirect('mainpage')

def encrypt_string(string):
    return hashlib.sha256(string.encode()).hexdigest()


def my_authenticate(username, password):
    password = encrypt_string(password)
    query = User.objects.filter(username=username) | User.objects.filter(email=username)
    if query.exists() and query[0].password == password:
        return query[0]
    else:
        return None

def login_user(request):
    username = request.POST.get('usernameinput', None)
    password = request.POST.get('passwordinput', None)
    otp_code = request.POST.get('otpinput', None)
    user = my_authenticate(username, password)
    if user is not None:
        if user.banned_until is not None and user.banned_until > date.today():
            return redirect('banned')
        if user.otp_secret:
            totp = pyotp.TOTP(user.otp_secret)
            if not totp.verify(otp_code):
                return redirect('login')
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

def block_user(request, pk):
    blockee = User.objects.get(pk=pk)
    blocker = User.objects.get(pk=request.session['userid'])
    blocker.blocking.add(blockee)
    blocker.save()
    # TODO: delete existing following relationship
    deleteFollow(pk, blocker.username)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unblock_user(request, pk):
    blockee = User.objects.get(pk=pk)
    blocker = User.objects.get(pk=request.session['userid'])
    blocker.blocking.remove(blockee)
    blocker.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def request_verification(request, pk):
    user = User.objects.get(pk=pk)
    if user.verified == 0:
        user.verified = 1
        user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def enable_2fa(request, pk):
    user = User.objects.get(pk=pk)
    if not user.otp_secret:
        user.otp_secret = pyotp.random_base32()
        user.save()
    return redirect('mainpage')

def disable_2fa(request, pk):
    user = User.objects.get(pk=pk)
    if user.otp_secret:
        user.otp_secret = ""
        user.save()
    return redirect('mainpage')
