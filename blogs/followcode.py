from .models import User, Post, Report, Tag, Follow

def addFollow(follower,following, tag):
    follow_list = Follow.objects.filter(follower=follower, following=following)
    if follow_list.count() > 0:
        follow = follow_list[0]
        follow.tags.add(tag)
    else:
        follow = Follow(follower=follower, following=following)
        follow.save()
        follow.tags.add(tag)


def removeFollow(follower,following, tag):
    follow_list = Follow.objects.filter(follower=follower, following=following)
    if follow_list.count() > 0:
        follow = follow_list[0]
        follow.tags.remove(tag)