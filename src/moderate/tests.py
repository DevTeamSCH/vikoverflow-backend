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
        self.moderator.user.is_staff = True
        self.moderator.user.save()

        self.admin = Profile.objects.create(user=User.objects.create(username='Admin'))
        self.admin.user.is_superuser = True
        self.admin.user.is_staff = True
        self.admin.user.save()

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

    @parameterized.expand([
        ('question', Question),
        ('answer', Answer),
        ('comment', Comment),
        ('profile', Profile),
        ('tag', Tag),
        ('course', Course)
    ])
    def test_create_report(self, model_name, model_class):
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

    def create_report(self, object_type, object_id):
        response = self.client.post(self.base_url, {
            "text": "Test report text",
            "object_type": object_type,
            "object_id": object_id})
        return response.data['pk']

    @parameterized.expand([
        ('question', Question, lambda instance: instance.is_visible),
        ('answer', Answer, lambda instance: instance.is_visible),
        ('comment', Comment, lambda instance: instance.is_visible),
        ('profile', Profile, lambda instance: instance.user.is_active),
        ('tag', Tag, lambda instance: False),
        ('course', Course, lambda instance: False)
    ])
    def test_approve_report(self, model_name, model_class, is_visible_func):
        model_instance = model_class.objects.first()
        self.client.force_login(self.moderator.user)
        report_id = self.create_report(model_name, model_instance.pk)
        response = self.client.post(''.join([self.base_url, str(report_id), '/approve/']))
        report = Report.objects.get(pk=report_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(is_visible_func(model_instance))
        self.assertFalse(report.is_closed())
        self.assertEqual(report.approved_by.count(), 1)
        self.assertEqual(report.comments.count(), 1)

        self.client.logout()
        self.client.force_login(self.admin.user)
        response = self.client.post(''.join([self.base_url, str(report_id), '/approve/']))
        report = Report.objects.get(pk=report_id)
        model_instance = model_class.objects.first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(is_visible_func(model_instance))
        self.assertTrue(report.is_closed())
        self.assertEqual(report.approved_by.count(), 2)
        self.assertEqual(report.comments.count(), 2)

