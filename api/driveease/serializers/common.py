from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import ContactListModel, FileUploadModel

User = get_user_model()


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploadModel
        fields = ['id', 'file']


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "user_reference", "first_name", "last_name", "email", "profile_picture"]


class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactListModel
        fields = '__all__'
