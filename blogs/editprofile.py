from .models import Post, User

def change_email(user_id,email):
    user = User.objects.get(id=user_id)
    user.email = email
    user.save()

def change_username(user_id,username):
    user = User.objects.get(id=user_id)
    user.username = username
    user.save()

def change_password(user_id,password):
    user = User.objects.get(id=user_id)
    user.password = password
    user.save()

def change_profile_pic(user_id,profile_pic):
    user = User.objects.get(id=user_id)
    user.profile_pic = profile_pic
    user.save()

def change_biography(user_id, biography):
    user = User.objects.get(id=user_id)
    user.biography = biography
    user.save()