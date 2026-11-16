from django.conf import settings
from django.db import models

from . import generate_log_reference


class AdminActivityLog(models.Model):
    log_reference = models.CharField(
        max_length=30, unique=True, default=generate_log_reference, editable=False
    )
    ACTION_CHOICES = [
        ("create", "Create"), ("update", "Update"),
        ("delete", "Delete"), ("status_change", "Status Change"),
    ]
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="activity_logs"
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    target_type = models.CharField(max_length=50)
    target_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.admin} - {self.action} - {self.target_type}"
