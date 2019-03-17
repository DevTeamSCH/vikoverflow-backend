from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from account.models import Profile


class ReportStatus:
    OPENED = "OPENED"
    CLOSED = "CLOSED"


class Report(models.Model):
    STATUS_CHOICES = (
        (ReportStatus.OPENED, _('Opened')),
        (ReportStatus.CLOSED, _('Closed')),
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True)
    text = models.TextField()
    reporter = models.ForeignKey(Profile, related_name='reports', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=255, default=ReportStatus.OPENED)
    approved_by = models.ManyToManyField(User)

    # Generic relations for reports
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.text

    def object_type(self):
        return self.content_type.model

    def close(self):
        self.status = ReportStatus.CLOSED
        self.closed_at = timezone.now()

    def reopen(self):
        self.status = ReportStatus.OPENED
        self.closed_at = None

    def is_closed(self):
        return self.status == ReportStatus.CLOSED


class ReportComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    text = models.TextField()
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text
