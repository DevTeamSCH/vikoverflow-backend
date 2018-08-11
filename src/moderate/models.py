from django.db import models
from django.utils.translation import gettext as _
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from account.models import Profile


class ModeratorComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    owner = models.ForeignKey(Profile, related_name='moderate_comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Report(models.Model):
    STATUS_CHOICES = (
        ('OPENED', _('Opened')),
        ('CLOSED', _('Closed')),
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(blank=True)
    text = models.TextField()
    reporter = models.ForeignKey(Profile, related_name='reports', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=255)

    # Generic relations for reports
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.text
