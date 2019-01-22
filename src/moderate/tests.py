from parameterized import parameterized
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from taggit.models import Tag

from account.models import Profile
from common.models import Votes
from moderate.models import Report
from moderate.serializers import ReportSerializer
from question.models import Question, Answer, Comment, Course


class ReportTestCase(APITestCase):

    base_url = "http://localhost:8000/api/v1/reports/"

    def setUp(self):
        self.user = Profile.objects.create(user=User.objects.create(username='Test user'))
        self.moderator = Profile.objects.create(user=User.objects.create(username='Moderator'))
        self.admin = Profile.objects.create(user=User.objects.create(username='Admin'))

        self.moderator.user.is_staff = True
        self.admin.user.is_superuser = True

        question = Question(
            title="Test question",
            owner=self.user,
            show_username=True,
            votes=Votes.objects.create()
        )
        question.save()

        Answer(
            text="Test answer",
            parent=question,
            owner=self.user,
            show_username=False,
            votes=Votes.objects.create(),
            is_accepted=False
        ).save()

        Comment(
            text="Test comment",
            parent_question=question,
            owner=self.user,
            show_username=False,
            votes=Votes.objects.create()
        ).save()

    # ------------------------
    # Reports
    # ------------------------

    @parameterized.expand([
        ('question', Question),
        ('answer', Answer),
        ('comment', Comment),
        ('profile', Profile),
        ('tag', Tag),
        ('course', Course)
    ])
    def test_report(self, model_name, model_class):
        model_object = model_class.objects.first()
        self.client.force_login(self.user.user)
        response = self.client.post(self.base_url, {
            "text": "Test report text",
            "object_type": model_name,
            "object_id": model_object.pk})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        report = Report.objects.get(pk=response.data['pk'])
        self.assertEqual(report.content_object, model_object)
        self.assertEqual(response.data, ReportSerializer(report).data)


# Create your tests here.
