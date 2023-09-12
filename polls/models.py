import datetime
from django.contrib.auth.models import User
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
    pub_date = models.DateTimeField('date published', auto_now_add=False)
    # pub_date default is set to be the current datetime.
    end_date = models.DateTimeField('end date', default=None, null=True, blank=True)
    # end_date can be null when the poll is intended to be available anytime after publication.

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        was_published_recently will return if the poll was published recently.
        The time span would be in the between of the current time and the day before the current time.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        is_published returns True if the current date is on or after question’s publication date.
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """
        can_vote returns True if voting is allowed for this question
        """
        now = timezone.now()
        if self.end_date is not None:
            return self.is_published() and now < self.end_date
        else:
            return self.is_published()


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
    # votes = models.IntegerField(default=0)

    @property
    def votes(self):
        """
        Count the votes for this choice.
        """
        return self.vote_set.count()

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    """
    Records a Vote of a Choice by a User
    """
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

