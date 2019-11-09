from .models import User, Post, Report, Tag, Follow, Chat, Message

def createChat(name, creator_id):
    creator = User.objects.get(id=creator_id)
    chat = Chat(creator=creator, name=name)
    chat.save()
    chat.members.add(creator)
    chat.save()

def addUser(chat_id, user_id):
    chat = Chat.objects.get(id=chat_id)
    user = User.objects.get(id=user_id)
    chat.members.add(user)
    chat.save()

def createMessage(creator_id, content, chat_id):
    creator = User.objects.get(id=creator_id)
    chat = Chat.objects.get(id=chat_id)
    message = Message(creator=creator,content=content,chat=chat)
    message.save()

def deleteMessage(message_id):
    message = Message.objects.get(id=message_id)
    message.delete()