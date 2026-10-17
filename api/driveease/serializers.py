import uuid

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Accounts, ContactListModel, Cars, FileUploadModel, Reviews, Booking, Payment, Feature, Notification, CarType

User = get_user_model()

#Common Serializers

class MiniCarSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Cars
        fields = (
            "car_id",
            "brand",
            "model",
            "image",
            "year",
        )

    def get_image(self, obj):
        return obj.meta.get("primary_image")

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "profile_picture"]

class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactListModel
        fields = '__all__'

class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = ["id", "name", "slug"]

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "name", "slug"]

class CarSerializer(serializers.ModelSerializer):
    unavailable_periods = serializers.SerializerMethodField()
    rental_count = serializers.IntegerField(read_only=True)

    car_type = serializers.SlugRelatedField(
        read_only=True,
        slug_field="slug",
    )

    features = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="slug",
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

class CarCreateSerializer(serializers.ModelSerializer):
    car_type = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=CarType.objects.all(),
        allow_null=True,
    )

    features = serializers.SlugRelatedField(
        many=True,
        slug_field="slug",
        queryset=Feature.objects.all(),
    )

    class Meta:
        model = Cars
        fields = [
            "car_id",
            "brand",
            "model",
            "year",
            "car_type",
            "price_per_day",
            "transmission",
            "engine",
            "fuel_type",
            "seats",
            "note",
            "meta",
            "status",
            "features",
        ]
        read_only_fields = ["car_id"]

    def create(self, validated_data):
        features = validated_data.pop("features", [])

        validated_data["car_id"] = str(uuid.uuid4())
        validated_data["created_by"] = self.context["request"].user

        car = Cars.objects.create(**validated_data)
        car.features.set(features)

        return car

class CarUpdateSerializer(serializers.ModelSerializer):
    car_type = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=CarType.objects.all(),
        allow_null=True,
    )

    features = serializers.SlugRelatedField(
        many=True,
        slug_field="slug",
        queryset=Feature.objects.all(),
    )

    class Meta:
        model = Cars
        fields = [
            "car_id",
            "brand",
            "model",
            "year",
            "car_type",
            "price_per_day",
            "transmission",
            "engine",
            "fuel_type",
            "seats",
            "note",
            "meta",
            "status",
            "features",
        ]
        read_only_fields = ["car_id"]

class AccountsSerializer(serializers.ModelSerializer):
    given_name = serializers.CharField(source='first_name')
    family_name = serializers.CharField(source='last_name')
    status = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    rentals = serializers.IntegerField(read_only=True)

    class Meta:
        model = Accounts
        fields = [
            'id',
            'email',
            'given_name',
            'family_name',
            'contact_number',
            'address',
            'profile_picture',
            'id_images',
            'date_joined',
            'status',
            'role',
            'rentals',
        ]

    def get_status(self, obj):
        if not obj.is_active:
            return 'Suspended'
        return 'Active'

    def get_role(self, obj):
        if obj.is_superuser:
            return 'Super Admin'
        if obj.is_staff:
            return 'Admin'
        return 'User'

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploadModel
        fields = ['id', 'file']

# Review Serializers

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

class AdminReviewSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    car = MiniCarSerializer(read_only=True)

    class Meta:
        model = Reviews
        fields = [
            'id',
            'car',
            'user',
            'rating',
            'text',
            'status',
            'created_at',
            'images',
            'helpful_count',
        ]

# Booking Serializers

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
            "year",
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

    payment_status = serializers.CharField(
        source="payments.status",
        read_only=True
    )

    class Meta:
        model = Booking
        fields = (
            "booking_reference",
            "status",
            "car",
            "user",
            "payment_status",
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

# Notification Serializers

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


