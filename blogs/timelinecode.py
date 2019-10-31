from .models import User, Post, Report, Tag, Follow

def get_timeline_posts(user):
    all_posts = [];
    user_posts = Post.objects.filter(creator=user)
    for post in user_posts:
        if post not in all_posts:
            all_posts.append(post)
    user_follows = Follow.objects.filter(follower=user)
    for follow in user_follows:
        for tag in follow.tags.all():
            if tag.name == '$all':
                tagged_posts = Post.objects.filter(creator=follow.following)
            else:
                tagged_posts = tag.posts.filter(creator=follow.following)
            for post in tagged_posts:
                if post not in all_posts:
                    all_posts.append(post)
    n = len(all_posts)
    for i in range(n):
        for j in range(0, n - i - 1):
            if all_posts[j].created < all_posts[j+1].created:
                all_posts[j], all_posts[j + 1] = all_posts[j + 1], all_posts[j]
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
            if tag.name == '$all':
                tagged_posts = Post.objects.filter(creator=follow.following)
            else:
                tagged_posts = tag.posts.filter(creator=follow.following)
            for post in tagged_posts:
                if post.tag_set.all().filter(name=tag_name).count() is 1:
                    if post not in all_posts:
                        all_posts.append(post)
    n = len(all_posts)
    for i in range(n):
        for j in range(0, n - i - 1):
            if all_posts[j].created < all_posts[j + 1].created:
                all_posts[j], all_posts[j + 1] = all_posts[j + 1], all_posts[j]
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
            if tag.name == '$all':
                tagged_posts = Post.objects.filter(creator=follow.following)
            else:
                tagged_posts = tag.posts.filter(creator=follow.following)
            for post in tagged_posts:
                if text in post.content:
                    if post not in all_posts:
                        all_posts.append(post)
    n = len(all_posts)
    for i in range(n):
        for j in range(0, n - i - 1):
            if all_posts[j].created < all_posts[j + 1].created:
                all_posts[j], all_posts[j + 1] = all_posts[j + 1], all_posts[j]
    return all_posts

def timeline_by_date(user, date):
    all_posts = []
    user_posts = Post.objects.filter(creator=user,created=date)
    for post in user_posts:
        if post not in all_posts:
            all_posts.append(post)
    user_follows = Follow.objects.filter(follower=user)
    for follow in user_follows:
        for tag in follow.tags.all():
            if tag.name == '$all':
                tagged_posts = Post.objects.filter(creator=follow.following,created=date)
            else:
                tagged_posts = tag.posts.filter(creator=follow.following,created=date)
            for post in tagged_posts:
                print (post.created)
                print (date)
                print (date is post.created)
                if post not in all_posts:
                    all_posts.append(post)
    n = len(all_posts)
    for i in range(n):
        for j in range(0, n - i - 1):
            if all_posts[j].created < all_posts[j + 1].created:
                all_posts[j], all_posts[j + 1] = all_posts[j + 1], all_posts[j]
    return all_posts