from django.contrib.contenttypes.models import ContentType
from rest_framework.fields import ChoiceField
from rest_framework.serializers import ModelSerializer

from account.models import Profile
from moderate.models import Report


class ReportSerializer(ModelSerializer):
    object_type = ChoiceField(['question', 'answer', 'comment', 'profile', 'tag', 'course'])

    class Meta:
        model = Report
        fields = ('created_at', 'updated_at', 'closed_at', 'text', 'reporter', 'status', 'object_id', 'object_type')


class ReportCreateSerializer(ModelSerializer):
    object_type = ChoiceField(['question', 'answer', 'comment', 'profile', 'tag', 'course'])

    class Meta:
        model = Report
        fields = ('text', 'object_id', 'object_type')

    def create(self, validated_data):
        report = Report(
            reporter=Profile.objects.get_or_create(user=self.context['request'].user)[0],
            text=validated_data['text'],
            object_id=validated_data['object_id']
        )

        if validated_data['object_type'] == 'question':
            report.content_type = ContentType.objects.get(app_label="question", model="question")
        elif validated_data['object_type'] == 'answer':
            report.content_type = ContentType.objects.get(app_label="question", model="answer")
        elif validated_data['object_type'] == 'comment':
            report.content_type = ContentType.objects.get(app_label="question", model="comment")
        elif validated_data['object_type'] == 'profile':
            report.content_type = ContentType.objects.get(app_label="account", model="profile")
        elif validated_data['object_type'] == 'tag':
            report.content_type = ContentType.objects.get(app_label='taggit', model='tag')
        elif validated_data['object_type'] == 'course':
            report.content_type = ContentType.objects.get(app_label="question", model='course')

        report.save()
        return report
