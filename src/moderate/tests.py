from parameterized import parameterized
from django.contrib.auth.models import User
from parameterized.parameterized import parameterized_class
from rest_framework import status
from rest_framework.test import APITestCase
from taggit.models import Tag

from account.models import Profile
from common.models import Votes
from moderate.models import Report
from moderate.serializers import ReportSerializer
from question.models import Question, Answer, Comment, Course


@parameterized_class(('model_name', 'model_class', 'is_visible_func'), [
    ('question', Question, lambda _, instance: instance.is_visible),
    ('answer', Answer, lambda _, instance: instance.is_visible),
    ('comment', Comment, lambda _, instance: instance.is_visible),
    ('profile', Profile, lambda _, instance: instance.user.is_active),
    ('tag', Tag, lambda _, instance: False),
    ('course', Course, lambda _, instance: False)
])
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

    def test_create_report(self):
        model_object = self.model_class.objects.first()
        self.client.force_login(self.user.user)
        response = self.client.post(self.base_url, {
            "text": "Test report text",
            "object_type": self.model_name,
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

    def test_approve_report(self):
        model_instance = self.model_class.objects.first()
        self.client.force_login(self.moderator.user)
        report_id = self.create_report(self.model_name, model_instance.pk)
        response = self.client.post(''.join([self.base_url, str(report_id), '/approve/']))
        report = Report.objects.get(pk=report_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.is_visible_func(model_instance))
        self.assertFalse(report.is_closed())
        self.assertEqual(report.approved_by.count(), 1)
        self.assertEqual(report.comments.count(), 1)

        self.client.logout()
        self.client.force_login(self.admin.user)
        response = self.client.post(''.join([self.base_url, str(report_id), '/approve/']))
        report = Report.objects.get(pk=report_id)
        model_instance = self.model_class.objects.first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.is_visible_func(model_instance))
        self.assertTrue(report.is_closed())
        self.assertEqual(report.approved_by.count(), 2)
        self.assertEqual(report.comments.count(), 2)

    def test_reject_report(self):
        model_instance = self.model_class.objects.first()
        self.client.force_login(self.moderator.user)
        report_id = self.create_report(self.model_name, model_instance.pk)
        response = self.client.post(''.join([self.base_url, str(report_id), '/reject/']))
        report = Report.objects.get(pk=report_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(report.is_closed())
        self.assertTrue(self.is_visible_func(self.model_class.objects.first()))

