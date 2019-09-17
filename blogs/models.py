from django.db import models

class User(models.Model):
    firstname   = models.CharField(max_length=50)
    lastname    = models.CharField(max_length=50)
    username    = models.CharField(max_length=50, unique=True)
    email       = models.EmailField()
    password    = models.CharField(max_length=50)
    birthday    = models.DateField()
    biography   = models.TextField(blank=True)
    profile_pic = models.ImageField(blank=True, upload_to="uploads/")

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_creator")
    likers  = models.ManyToManyField(User, related_name="post_liker")
    content = models.TextField()
    created = models.DateField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    posts = models.ManyToManyField(Post)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    # if tags is empty, this means the user follows *all* tags by that user
    tags = models.ManyToManyField(Tag)
    # TODO: if we allow posts with no tags, we need a way to allow a user to follow
    # tagless posts - since tags can't be empty in name, we have another field
    # Alternatively, we could allow empty tags, and set that if no other tags present.
    #follow_empty = models.BooleanField()
    # TODO: allow actions for newly created tags (e.g. auto follow new tags y/n)
