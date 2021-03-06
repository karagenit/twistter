# Generated by Django 2.2.4 on 2019-11-30 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0028_auto_20191127_0012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='message',
            name='pic',
            field=models.ImageField(blank=True, upload_to='pics/'),
        ),
        migrations.AddField(
            model_name='user',
            name='chat_privacy',
            field=models.CharField(default='anyone', max_length=50),
            preserve_default=False,
        ),
    ]
