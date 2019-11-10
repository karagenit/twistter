from django.db import models

###
# Verified Codes:
# 0: Unverified
# 1: Verification Requested
# 2: Verified
class User(models.Model):
    firstname    = models.CharField(max_length=50)
    lastname     = models.CharField(max_length=50)
    username     = models.CharField(max_length=50, unique=True)
    email        = models.EmailField(unique=True)
    password     = models.CharField(max_length=64)
    birthday     = models.DateField(blank=True, null=True)
    biography    = models.TextField(default="This user has not entered a biography!", max_length=120, blank=True)
    profile_pic  = models.ImageField(upload_to='images/', blank=True)
    banned_until = models.DateField(blank=True, null=True)
    blocking     = models.ManyToManyField("User", blank=True)
    private      = models.BooleanField(default=False)
    verified     = models.IntegerField(default=0)

###
# TODO: assert that every post has 1+ tags (includes empty tag)
#
class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_creator")
    likers  = models.ManyToManyField(User, related_name="post_liker", blank=True)
    image   = models.ImageField(upload_to='pictures/', blank=True)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    quote   = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)

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
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    tags = models.ManyToManyField(Tag)

class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()

class Chat(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_creator")

class Message(models.Model):
    content = models.CharField(max_length=200)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_creator")
    created = models.DateTimeField(auto_now_add=True)
