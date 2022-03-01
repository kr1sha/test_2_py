from django.utils import timezone
import datetime

from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='question text')
    published_date = models.DateTimeField(verbose_name='date published', auto_now_add=True)

    def __str__(self):
        return str(self.question_text)

    def was_published_recently(self):
        return self.published_date > timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='question')
    choice_text = models.CharField(max_length=200, verbose_name='choice text')
    votes = models.PositiveIntegerField(default=0, verbose_name='number of votes')

    def __str__(self):
        return str(self.choice_text)


q = Question(question_text="what's up?")
from test_app.models import Question, Choice
