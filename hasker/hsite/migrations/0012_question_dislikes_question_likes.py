# Generated by Django 4.0.4 on 2022-05-08 14:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hsite', '0011_answervotes_answer_users_votes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='dislikes',
            field=models.ManyToManyField(related_name='user_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='likes',
            field=models.ManyToManyField(related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
