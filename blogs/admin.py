from django.contrib import admin

from .models import User, Post, Tag, Follow, Report

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(Report)
