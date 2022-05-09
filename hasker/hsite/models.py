import os

# from enum import unique
from django.db import models
from django.db.models import Count
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import datetime, timezone
from uuid import uuid4
from PIL import Image


def unique_fname(instance, filename):
    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join('profile_images', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default-avatar.png', upload_to=unique_fname)

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()
        try:
            img = Image.open(self.avatar.path)

            if img.height > 100 or img.width > 100:
                new_img = (100, 100)
                img.thumbnail(new_img)
                img.save(self.avatar.path)
        except FileNotFoundError:
            pass


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    likes = models.ManyToManyField(User, related_name="user_q_likes", blank=True)
    dislikes = models.ManyToManyField(User, related_name="user_q_dislikes", blank=True)
    # users_votes = models.ManyToManyField(User, related_name="user_q_votes", through='QuestionVotes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("question", kwargs={"pk": self.pk})

    def get_q_age(self):
        td = datetime.now(tz=timezone.utc) - self.pub_date
        sec = round(td.total_seconds())
        if sec < 60:
            return "now"
        elif sec < 3600:
            return f"{sec//60} min ago"
        elif sec < 3600 * 24:
            return f"{sec//3600} hour ago"
        elif sec < 3600 * 24 * 30:
            return f"{sec//(3600*24)} day ago"
        else:
            return f"{sec//(3600*24*30)} month ago"

    def get_votes(self):
        q = Question.objects.filter(pk=self.pk)
        q = q.annotate(votes=Count('likes', distinct=True) - Count('dislikes', distinct=True))
        return q[0].votes if q else 0


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    likes = models.ManyToManyField(User, related_name="user_a_likes", blank=True)
    dislikes = models.ManyToManyField(User, related_name="user_a_dislikes", blank=True)
    # users_votes = models.ManyToManyField(User, related_name="user_a_votes", through='AnswerVotes')

    def __str__(self):
        return self.title


# class QuestionVotes(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     score = models.SmallIntegerField()

#     class Meta:
#         unique_together = [['user', 'question']]


# class AnswerVotes(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
#     score = models.SmallIntegerField()

#     class Meta:
#         unique_together = [['user', 'answer']]


class Tag(models.Model):
    tag = models.CharField(max_length=30)
    question = models.ManyToManyField(Question)

    def __str__(self):
        return self.tag
