from .models import User, Post, Report, Tag, Follow, Chat, Message

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
    for member in chat.members.all():
        if user in member.blocking.all():
            return
        if member in user.blocking.all():
            return
    chat.members.add(user)

def removeUser(chat_id, user_id):
    chat = Chat.objects.get(id=chat_id)
    user = User.objects.get(id=user_id)
    chat.members.add(user)

def createMessage(creator_id, content, chat_id):
    creator = User.objects.get(id=creator_id)
    chat = Chat.objects.get(id=chat_id)
    message = Message(creator=creator,content=content,chat=chat)
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