# Generated by Django 2.2.4 on 2019-11-01 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0020_auto_20191031_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
