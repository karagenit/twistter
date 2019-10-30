from .models import User, Post, Report, Tag, Follow

def addFollow(follower_id,following_name, tag_name):
    follower = User.objects.get(id=follower_id)
    following_query = User.objects.filter(username=following_name)
    if following_query.exists():
        following = following_query[0]
    else:
        return
    tag_query = Tag.objects.filter(name=tag_name)
    if tag_query.exists():
        tag = tag_query[0]
    else:
        tag = Tag(name=tag_name)
        tag.save()
    follow_list = Follow.objects.filter(follower=follower, following=following)
    if follow_list.count() > 0:
        follow = follow_list[0]
    else:
        follow = Follow(follower=follower, following=following)
        follow.save()
    if tag.name is '$all':
        follow.tags.delete()
    if follow.tags.filter(name='$all').exists():
        return
    follow.tags.add(tag)


def removeFollow(follower_id,following_name, tag_name):
    follower = User.objects.get(id=follower_id)
    following_query = User.objects.filter(username=following_name)
    if following_query.exists():
        following = following_query[0]
    else:
        return
    follow_list = Follow.objects.filter(follower=follower, following=following)
    tag_query = Tag.objects.filter(name=tag_name)
    if not tag_query.exists():
        return
    tag = tag_query[0]
    if follow_list.count() > 0:
        follow = follow_list[0]
        follow.tags.remove(tag)
        if follow.tags.count() is 0:
            follow.delete()

def getFollowing(user_id):
    user = User.objects.get(id=user_id)
    following_list_query = Follow.objects.filter(following=user)
    following_list = []
    for follow in following_list_query:
        following_list.append(follow)
    return following_list

def getFollowers(user_id):
    user = User.objects.get(id=user_id)
    follower_list_query = Follow.objects.filter(follower=user)
    follower_list = []
    for follow in follower_list_query:
        follower_list.append(follow)
    return follower_list