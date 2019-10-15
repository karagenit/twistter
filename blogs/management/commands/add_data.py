from django.core.management.base import BaseCommand

from blogs.models import User, Post, Report
from blogs.views import encrypt_string

class Command(BaseCommand):
    help = 'Preloads Initial Test Data'

    def handle(self, *args, **options):
        password = encrypt_string('Password123')

        u1 = User(firstname='Caleb', lastname='Smith', username='smit3484',
             email='caleb@test.com', password=password, biography='Sample Bio')
        u1.save()
        u2 = User(firstname='John', lastname='Doe', username='jdoe',
             email='john@test.com', password=password, biography='Hello')
        u2.save()

        Post(creator=u1, content='First Post Ever').save()
        Post(creator=u1, content='Second Post').save()
        p3 = Post(creator=u2, content="John's Post")
        p3.save()

        Report(reporter=u1, post=p3).save()
