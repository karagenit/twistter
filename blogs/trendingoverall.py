from .models import Post
from django.db.models import Count
from operator import attrgetter

def get_trending():
    post_array = []
    all_posts = Post.objects.all().annotate(num_likes=Count('likers'))
    for post in all_posts:
        post_array.append(post)
    post_array.sort(key= attrgetter('num_likes'), reverse = True)
    return all_posts

