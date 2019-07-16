from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ParseError
from rest_framework.fields import ChoiceField
from rest_framework.serializers import ModelSerializer

from account.models import Profile
from moderate.models import Report, ReportComment


class ModeratorCommentSerializer(ModelSerializer):
    class Meta:
        model = ReportComment
        fields = ("pk", "created_at", "text", "owner")


class ReportSerializer(ModelSerializer):
    object_type = ChoiceField(
        ["question", "answer", "comment", "profile", "tag", "course"]
    )
    comments = ModeratorCommentSerializer(many=True, required=False)

    class Meta:
        model = Report
        fields = (
            "pk",
            "created_at",
            "updated_at",
            "closed_at",
            "text",
            "reporter",
            "status",
            "object_id",
            "object_type",
            "comments",
        )
        read_only_fields = (
            "pk",
            "created_at",
            "updated_at",
            "closed_at",
            "reporter",
            "status",
            "comments",
        )

    def create(self, validated_data):
        report = Report(
            reporter=Profile.objects.get_or_create(user=self.context["request"].user)[
                0
            ],
            text=validated_data["text"],
            object_id=validated_data["object_id"],
        )

        if validated_data["object_type"] == "question":
            report.content_type = ContentType.objects.get(
                app_label="question", model="question"
            )
        elif validated_data["object_type"] == "answer":
            report.content_type = ContentType.objects.get(
                app_label="question", model="answer"
            )
        elif validated_data["object_type"] == "comment":
            report.content_type = ContentType.objects.get(
                app_label="question", model="comment"
            )
        elif validated_data["object_type"] == "profile":
            report.content_type = ContentType.objects.get(
                app_label="account", model="profile"
            )
        elif validated_data["object_type"] == "tag":
            report.content_type = ContentType.objects.get(
                app_label="question", model="questiontag"
            )

        if report.content_object is None:
            raise ParseError()

        report.save()
        return report
