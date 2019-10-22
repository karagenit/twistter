from django.db import models

class User(models.Model):
    firstname    = models.CharField(max_length=50)
    lastname     = models.CharField(max_length=50)
    username     = models.CharField(max_length=50, unique=True)
    email        = models.EmailField(unique=True)
    password     = models.CharField(max_length=50)
    birthday     = models.DateField(null=True)
    biography    = models.TextField(default="Enter Bio", max_length=120, blank=True)
    profile_pic  = models.ImageField(upload_to='images/')
    banned_until = models.DateField(null=True)

###
# TODO: assert that every post has 1+ tags (includes empty tag)
#
class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_creator")
    likers  = models.ManyToManyField(User, related_name="post_liker", blank=True)
    content = models.TextField()
    created = models.DateField(auto_now_add=True)

###
# Note: the blank tag will exist and is a unique tag.
# Users may not add a blank tag to their posts - the blank tag is
# added automatically when a post is created without other tags.
#
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=True)
    posts = models.ManyToManyField(Post)

###
# Note: if 'tags' is empty, this means the user follows *all* posts by that user
# this differs from just following all of the user's tags, as it includes future tags too.
# Users can follow the 'empty' special tag to see posts that have no tags.
#
# TODO: allow users to follow just tags without a person?
#
# User's timelines consist of all posts by posters they follow that are tagged with at
# least one of the tags that user follower for that poster.
#
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    tags = models.ManyToManyField(Tag)

class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
