from django.test import TestCase
import datetime
from .models import Question
from django.utils import timezone


# Create your tests here.
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
        was_published() method returns False for questions whose pub_date
        is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=2)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published() method return True if a question is 1 day or
        less recently
        """
        time = timezone.now() - datetime.timedelta(hours=3)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)