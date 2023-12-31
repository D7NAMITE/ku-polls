from django.test import TestCase
import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

    def test_pub_date_default(self):
        question = create_question(question_text="Is this defaulted.", days=0)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,question.question_text)


    def test_is_published_future_question(self):
        """
        is_published must be able to check the question that will be published
        in the future as a question that is not published yet.
        """
        future_question = create_question(question_text='This is a question from the future.', days=3)
        self.assertFalse(future_question.is_published())


    def test_is_published_default_pub_date(self):
        """
        is_published must be able to check the question that published in the default(now)
        as a question that is published.
        """
        question = create_question(question_text='This is a question from NOW.', days=0)
        self.assertTrue(question.is_published())


    def test_is_published_past_question(self):
        """
                is_published must be able to check the question that published in the past
                as a question that is already published.
        """
        question = create_question(question_text='This is a question from the past.', days=-3)
        self.assertTrue(question.is_published())

    def test_can_vote_none_end_date(self):
        """
        can_vote must return True if the end date is None(default value for end_date).
        """
        question = create_question(question_text='This is a question to test None end_date', days=-3)
        question.end_date = None
        self.assertTrue(question.can_vote())


    def test_can_vote_past_end_date(self):
        """
        can_vote must return False if the end date is already passed.
        """
        question = create_question(question_text='This is a question to test past end_date', days=-3)
        now = timezone.now()
        question.end_date = now - datetime.timedelta(days=1)
        self.assertFalse(question.can_vote())


    def test_can_vote_default_end_date(self):
        """
        can_vote must return True if the end date is leave blank as it must set as defalut(None)
        """
        question = create_question(question_text='This is a question to test blank end_date', days=-3)
        self.assertTrue(question.can_vote())


    def test_can_vote_future_pub_date(self):
        """
        can_vote must return False if the question is not yet published
        """
        question = create_question(question_text='This is a question to test blank end_date', days=3)
        question.end_date = None
        self.assertFalse(question.can_vote())


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
