from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ContactListModel, Cars, FileUploadModel, Reviews, Booking, Payment

User = get_user_model()

class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactListModel
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = '__all__'  

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "profile_picture"]

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploadModel
        fields = ['id', 'file']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    helpful = serializers.SerializerMethodField()
    is_mine = serializers.BooleanField(read_only=True)

    class Meta:
        model = Reviews
        fields = ["id", "user", "car", "rating", "text", "helpful_count", "images", "created_at", "helpful","is_mine"]

    def get_helpful(self, obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return False

        return obj.helpful_votes.filter(user=request.user).exists()

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['booking_reference', 'created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']