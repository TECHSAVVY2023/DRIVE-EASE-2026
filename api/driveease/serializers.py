from rest_framework import serializers
from .models import ContactListModel, Cars, FileUploadModel

class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactListModel
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = '__all__'  

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploadModel
        fields = ['id', 'file']