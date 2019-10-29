from .models import User, Post, Report, Tag, Follow, Comment

def add_comment(post,commenter,content):
    comment = Comment(commenter=commenter,post=post,content=content)
    comment.save()