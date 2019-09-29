from .models import Post, User

def make_post(content,user_id):
    user = User.objects.get(id=user_id)
    post = Post(content=content, creator=user)
    post.save()