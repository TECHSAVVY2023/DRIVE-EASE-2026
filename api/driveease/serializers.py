from rest_framework import serializers
from .models import ContactListModel, Cars, CarImage

class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactListModel
        fields = '__all__'

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'is_primary']

class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Cars
        fields = '__all__'
