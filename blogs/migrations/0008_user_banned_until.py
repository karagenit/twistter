# Generated by Django 2.2.4 on 2019-10-15 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_auto_20191015_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='banned_until',
            field=models.DateField(null=True),
        ),
    ]
