import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    This class will represent all the fields within the Question
    as a model which the field inside the Question are
    question_text: the question of that poll,
    pub_date: the date and time of publication of the poll.
    end_date: the date and time of the poll's ending.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)  # pub_date default is set to be the current datetime.
    end_date = models.DateTimeField('end date', null=True)  # end_date can be null when the poll is intended to be available anytime after publication.

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        was_published_recently will return if the poll was published recently.
        The time span would be in the between of the current time and the day before the current time.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """
        This class will represent all the fields within the Choice
        as a model which the field inside the Choice are
        question: the question that is the root of the choice.
        choice_text: the choice of the root question.
        votes: the amount of votes of the choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
