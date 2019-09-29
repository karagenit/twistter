from django.db import models

class User(models.Model):
    firstname   = models.CharField(max_length=50)
    lastname    = models.CharField(max_length=50)
    username    = models.CharField(max_length=50)
    email       = models.EmailField()
    password    = models.CharField(max_length=50)
    birthday    = models.DateField()
    biography   = models.TextField()
    profile_pic = models.ImageField(upload_to="uploads/")
