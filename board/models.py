from django.contrib.auth.models import User
from django.db import models

# TODO: date 필드 수정
#  auto_add, auto_add_now 추가하기

# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    voter = models.ManyToManyField(User, related_name='voter_question')
    hit = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, on_delete=models.CASCADE)
