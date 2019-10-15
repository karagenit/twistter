from .models import Post, User, Tag

def addtag(self, name, post):
    try:
        tag = Tag.objects.get(name=name)
    except ObjectDoesNotExist:
        tag = Tag(name=name)
        tag.save()
    tag.posts.add(post)
    tag.save()
