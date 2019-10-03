from django import template

from ..models import User, Post

register = template.Library()

@register.simple_tag
def user_post_content(user, post_index):
    return user.post_creator.all()[post_index].content

@register.simple_tag
def user_posts(user):
    return user.post_creator.all()
