from .models import Post, User

#gets all posts made by the user specified by his ID
def get_posts(user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(creator=user)
    post_info = []
    for post in posts:
        post_info.append([post.content,post.created])
    return post_info # returns a list of [content, date created] lists


