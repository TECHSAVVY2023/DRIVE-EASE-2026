from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ContactListModel, Cars, FileUploadModel, Reviews, Booking, Payment, Feature, Notification

User = get_user_model()

class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactListModel
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    unavailable_periods = serializers.SerializerMethodField()

    features = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Cars
        fields = "__all__"

    def get_unavailable_periods(self, obj):
        bookings = obj.bookings.filter(
            status__in=[
                "pending_approval",
                "confirmed",
                "picked_up",
            ]
        )

        # print(obj.car_id, bookings.count())

        return [
            {
                "pickup_date": booking.pickup_date,
                "return_date": booking.return_date,
                "status": booking.status,
            }
            for booking in bookings
        ]

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

class TransactionCarSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Cars
        fields = (
            "car_id",
            "brand",
            "model",
            "image",
        )

    def get_image(self, obj):
        return obj.meta.get("primary_image")

class TransactionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "contact_number",
            "address",
            "id_images",
        )

class TransactionSerializer(serializers.ModelSerializer):
    car = TransactionCarSerializer(read_only=True)
    user = TransactionUserSerializer(read_only=True)

    payment_method = serializers.CharField(
        source="payments.payment_method",
        read_only=True
    )

    class Meta:
        model = Booking
        fields = (
            "booking_reference",
            "status",
            "car",
            "user",
            "payment_method",
            "created_at",
            "pending_approval_at",
            "confirmed_at",
            "picked_up_at",
            "returned_at",
            "completed_at",
            "cancelled_at",
            "cancel_reason",
            "daily_rate",
            "number_of_days",
            "subtotal",
            "discount",
            "total_price",
            "pickup_date",
            "return_date",
            "pickup_location",
            "return_location",
        )

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class NotificationBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "booking_reference",
            "status",
        ]

class NotificationSerializer(serializers.ModelSerializer):
    booking = NotificationBookingSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "title",
            "message",
            "action_url",
            "booking",
            "is_read",
            "read_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "notification_type",
            "title",
            "message",
            "action_url",
            "booking",
            "is_read",
            "read_at",
            "created_at",
        ]


