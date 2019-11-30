from .models import User, Post, Report, Tag, Follow, Chat, Message
from .followcode import getFollowing, getFollowers

def createChat(name, creator_id):
    creator = User.objects.get(id=creator_id)
    chat = Chat(creator=creator, name=name)
    chat.save()
    chat.members.add(creator)
    return chat

def deleteChat(chat_id, user_id):
    chat = Chat.objects.get(id=chat_id)
    if chat.creator.id is user_id:
        chat.delete()

def addUser(chat_id, user_id):
    chat = Chat.objects.get(id=chat_id)
    user = User.objects.get(id=user_id)
    if user.chat_privacy == 'Follow':
        creator = chat.creator
        following = getFollowing(user.id)
        followers = getFollowers(user.id)
        follow_users = []
        for follow in following:
            follow_users.append(follow.following)
        for follow in followers:
            follow_users.append(follow.follower)
        if creator not in follow_users:
            print("no follow")
            return
        print("follow")
    if user.chat_privacy == 'None':
        print('None')
        return
    for member in chat.members.all():
        if user in member.blocking.all():
            return
        if member in user.blocking.all():
            return
    chat.members.add(user)

def removeUser(chat_id, user_id):
    chat = Chat.objects.get(id=chat_id)
    user = User.objects.get(id=user_id)
    chat.members.remove(user)

def createMessage(creator_id, content, chat_id, image):
    creator = User.objects.get(id=creator_id)
    chat = Chat.objects.get(id=chat_id)
    message = Message(creator=creator, content=content, chat=chat, pic=image)
    message.save()

def deleteMessage(message_id):
    message = Message.objects.get(id=message_id)
    message.delete()

def getChats(user_id):
    chats = []
    for chat in Chat.objects.all():
        user_query = chat.members.all().filter(id=user_id)
        if user_query.exists():
            chats.append(chat)
    return chats