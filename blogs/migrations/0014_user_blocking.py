# Generated by Django 2.2.4 on 2019-10-29 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0013_auto_20191026_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blocking',
            field=models.ManyToManyField(blank=True, to='blogs.User'),
        ),
    ]
