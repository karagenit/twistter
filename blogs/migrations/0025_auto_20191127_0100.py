# Generated by Django 2.2.4 on 2019-11-27 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0024_user_otp_secret'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
