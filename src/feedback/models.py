from django.db import models
from django.utils.translation import gettext as _


class Ticket(models.Model):
    TICKET_TYPES = (
        ('BUG', _('Bug')),
        ('FEATURE', _('Feature request')),
    )

    title = models.CharField(max_length=255)
    text = models.TextField()
    # NOTE: type is a reserved keyword
    kind_of = models.CharField(max_length=255, choices=TICKET_TYPES)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"[{self.TICKET_TYPES[self.kind_of]}] {self.title}"
