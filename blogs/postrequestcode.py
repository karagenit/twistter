from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import IntegrityError
from django.urls import reverse

from datetime import date

from .models import User, Post, Report, Tag, Follow, Topic
from .commentcode import add_comment
from .getposts import get_posts
from .deleteuser import delete_user
from .tagcode import addtag, removetag
from .followcode import addFollow, removeFollow
from .timelinecode import timeline_by_tag, get_timeline_posts, timeline_by_text
import hashlib

def post_request_from_post(self,request):
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
            addtag(name, post)
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
        for usr in post.likers.all():
            print (usr.username)
            if usr.username == user.username:
                post.likers.remove(user)
                return
        post.likers.add(user)
    if 'followuser' in request.POST:
        follower_id = self.request.session.get('userid')
        following_name = request.POST.get('followuser')
        tag_name = request.POST.get('followtag')
        if request.POST.get('Following') is '1':
            addFollow(follower_id, following_name, tag_name)
        else:
            removeFollow(follower_id, following_name, tag_name)
        #follower = User.objects.get(id=follower_id)
        #follow_list = Follow.objects.filter(follower=follower)
        #for follow in follow_list:
        #    print (follow.following.username)
        #    for tag in follow.tags.all():
        #        print (tag.name)
    if 'add_comment' in request.POST:
        commenter_id = self.request.session.get('userid')
        commenter = User.objects.get(id=commenter_id)
        post_id = request.POST.get('add_comment_id', None)
        post = Post.objects.get(id=post_id)
        content = request.POST.get('add_comment', None)
        add_comment(post, commenter, content)
    if 'quote_post_text' in request.POST:
        tags = request.POST.get('quote_post_tag', None).split(",")
        content = request.POST.get('quote_post_text', None)
        user = User.objects.get(id=self.request.session.get('userid'))
        quoted_post = Post.objects.get(id=request.POST.get('quote_post_id', None))
        if not content:
            return redirect('mainpage')
        post = Post(content=content, creator=user)
        post.quote = quoted_post
        post.save()
        for tag in tags:
            addtag(tag, post)
    if 'add_interest' in request.POST:
        user_id = self.request.session.get('userid')
        name = request.POST.get('add_interest')
        if not name:
            return
        topic = Topic(name=name)
        topic.save()
        user = User.objects.get(id=user_id)
        user.interests.add(topic)
        user.save()
