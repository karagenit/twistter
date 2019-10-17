from .models import Post, User, Tag

def addtag(name, post):
    try:
        tag = Tag.objects.get(name=name)
    except:
        tag = Tag(name=name)
        tag.save()
    tag.posts.add(post)
    tag.save()

def get_tags_by_post(post):
    return post.tag_set.all()

def get_posts_by_tag(tag):
    return tag.posts.all()
