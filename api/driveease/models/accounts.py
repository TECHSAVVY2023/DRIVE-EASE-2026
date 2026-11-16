from django.contrib.auth.models import AbstractUser
from django.db import models

from . import default_user_id, generate_user_reference


class Accounts(AbstractUser):
    user_reference = models.CharField(
        max_length=30, unique=True, default=generate_user_reference, editable=False
    )
    contact_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.URLField(blank=True, null=True)
    id_images = models.JSONField(default=default_user_id, blank=True)

    def __str__(self):
        return self.username
