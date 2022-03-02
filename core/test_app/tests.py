import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
    """
    Create the question with the given question_text and
    published the given number of days offset to now
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, published_date=time)


class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        Was_published_recently return False for future published_date
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(published_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        Was_published_recently return False for published_date older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(published_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        Was_published_recently return True for published_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(published_date=time)
        self.assertIs(future_question.was_published_recently(), True)

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('test:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a published_date in the past are displayed on the index page
        """
        create_question(question_text="past_question", days=-30)
        response = self.client.get(reverse("test:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past_question>'])

    def test_future_question(self):
        """
        Questions with future published_date aren't displayed on the index page
        """
        create_question(question_text="future_question", days=30)
        response = self.client.get(reverse("test:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        even if both past and future questions exist, only past questions are displayed
        """
        create_question(question_text="future_question", days=30)
        create_question(question_text="past_question", days=-30)
        response = self.client.get(reverse("test:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past_question>'])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions
        """
        create_question(question_text="past_question_1", days=-30)
        create_question(question_text="past_question_2", days=-5)
        response = self.client.get(reverse("test:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: past_question_2>', '<Question: past_question_1>'])


class QuestionDetailViewTest(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a published date in the future returns a 404 not found
        """
        future_question = create_question(question_text="Future question", days=5)
        url = reverse("test:question_detail", args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a published date in the past displays the question's text
        """
        past_question = create_question(question_text="Past question", days=-5)
        url = reverse("test:question_detail", args=(past_question.id, ))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


