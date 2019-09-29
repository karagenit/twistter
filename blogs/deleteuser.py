from .models import Post, User

#deletes user and all posts by user from database
def delete_user(user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(creator=user)
    for post in posts:
        post.delete()
    user.delete()