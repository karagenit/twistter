from .models import User, Post, Report, Tag, Follow
from django.db.models import Count
from operator import attrgetter
import datetime

def get_timeline_posts(user):
    all_posts = [];
    user_posts = Post.objects.filter(creator=user)
    for post in user_posts:
        if post not in all_posts:
            all_posts.append(post)
    user_follows = Follow.objects.filter(follower=user)
    for follow in user_follows:
        for tag in follow.tags.all():
            following_posts = Post.objects.filter(creator=follow.following)
            if follow.all:
                tagged_posts = following_posts
            else:
                tagged_posts = tag.posts.filter(creator=follow.following)
            for post in following_posts:
                if post.created > user.curr_time_line_view and post not in all_posts:
                    all_posts.append(post)
            for post in tagged_posts:
                if post not in all_posts:
                    all_posts.append(post)
    all_posts.sort(key=lambda x: x.created.timestamp(), reverse=True)
    return all_posts

def timeline_by_tag(user,tag_name):
    tag = Tag.objects.get(name=tag_name)
    all_posts = [];
    user_posts = Post.objects.filter(creator=user)
    for post in user_posts:
        if post.tag_set.all().filter(name=tag_name).count() is 1:
            if post not in all_posts:
                all_posts.append(post)
    user_follows = Follow.objects.filter(follower=user)
    for follow in user_follows:
        for tag in follow.tags.all():
            if follow.all:
                tagged_posts = Post.objects.filter(creator=follow.following)
            else:
                tagged_posts = tag.posts.filter(creator=follow.following)
            for post in tagged_posts:
                if post.tag_set.all().filter(name=tag_name).count() is 1:
                    if post not in all_posts:
                        all_posts.append(post)
    all_posts.sort(key=lambda x: x.created.timestamp(), reverse=True)
    return all_posts

def timeline_by_text(user, text):
    all_posts = [];
    user_posts = Post.objects.filter(creator=user)
    for post in user_posts:
        if text in post.content:
            if post not in all_posts:
                all_posts.append(post)
    user_follows = Follow.objects.filter(follower=user)
    for follow in user_follows:
        for tag in follow.tags.all():
            if follow.all:
                tagged_posts = Post.objects.filter(creator=follow.following)
            else:
                tagged_posts = tag.posts.filter(creator=follow.following)
            for post in tagged_posts:
                if text in post.content:
                    if post not in all_posts:
                        all_posts.append(post)
    all_posts.sort(key=lambda x: x.created.timestamp(), reverse=True)
    return all_posts

def timeline_by_date(user, date):
    all_posts = []
    try:
        date_array = date.split('/')
        user_posts = Post.objects.filter(creator=user,created__contains=datetime.date(int(date_array[2]), int(date_array[0]), int(date_array[1])))
    except:
        return None
    for post in user_posts:
        if post not in all_posts:
            all_posts.append(post)
    user_follows = Follow.objects.filter(follower=user)
    for follow in user_follows:
        for tag in follow.tags.all():
            if follow.all:
                tagged_posts = Post.objects.filter(creator=follow.following,created__contains=datetime.date(int(date_array[2]), int(date_array[0]), int(date_array[1])))
            else:
                tagged_posts = tag.posts.filter(creator=follow.following,created__contains=datetime.date(int(date_array[2]), int(date_array[0]), int(date_array[1])))
            for post in tagged_posts:
                print (post.created)
                print (date)
                print (date is post.created)
                if post not in all_posts:
                    all_posts.append(post)
    all_posts.sort(key=lambda x: x.created.timestamp(), reverse=True)
    return all_posts

def timeline_by_trending(user):
    all_posts = []
    user_posts = Post.objects.filter(creator=user).annotate(num_likes=Count('likers'))
    for post in user_posts:
        if post not in all_posts:
            all_posts.append(post)
    user_follows = Follow.objects.filter(follower=user)
    for follow in user_follows:
        for tag in follow.tags.all():
            if follow.all:
                tagged_posts = Post.objects.filter(creator=follow.following).annotate(num_likes=Count('likers'))
            else:
                tagged_posts = tag.posts.filter(creator=follow.following).annotate(num_likes=Count('likers'))
            for post in tagged_posts:
                if post not in all_posts:
                    all_posts.append(post)
    all_posts.sort(key= attrgetter('num_likes'), reverse = True)
    return all_posts
