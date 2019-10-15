from .models import Post, User, Tag

def addtag(name, post):
    try:
        tag = Tag.objects.get(name=name)
    except tag.DoesNotExist:
        tag = Tag(name=name)
        tag.save()
    tag.posts.add(post)
    tag.save()
