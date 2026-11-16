from django.db import models
from django.template import defaultfilters
from storages.backends.s3boto3 import S3Boto3Storage

from . import unique_upload_path


class FileUploadModel(models.Model):
    file = models.FileField(storage=S3Boto3Storage(), upload_to=unique_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class ContactListModel(models.Model):
    contact_id = models.CharField(max_length=255, blank=True, null=True, default='')
    firstname = models.CharField(max_length=255, blank=True, null=True, default='')
    lastname = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_email = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_number = models.CharField(max_length=255, blank=True, null=True, default='')
    message = models.CharField(max_length=500, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def created_at_formatted(self):
        return defaultfilters.date(self.created_at, 'M d, Y')
