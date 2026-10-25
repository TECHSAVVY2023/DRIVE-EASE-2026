import uuid

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Accounts, ContactListModel, Cars, FileUploadModel, Reviews, Booking, Payment, Feature, Notification, CarType, AdminActivityLog

User = get_user_model()

#Common Serializers

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploadModel
        fields = ['id', 'file']

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

# Account Serializers

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

class AdminEditAccountSerializer(serializers.ModelSerializer):
    given_name = serializers.CharField(
        source="first_name",
        required=False,
        allow_blank=True,
        max_length=150,
    )
    family_name = serializers.CharField(
        source="last_name",
        required=False,
        allow_blank=True,
        max_length=150,
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )
    contact_number = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=20,
    )
    address = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    remove_profile_picture = serializers.BooleanField(
        required=False,
        default=False,
        write_only=True,
    )
    profile_removal_reason = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    remove_id_images = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list,
        write_only=True,
    )
    id_removal_reason = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    class Meta:
        model = Accounts
        fields = [
            "given_name",
            "family_name",
            "email",
            "contact_number",
            "address",
            "remove_profile_picture",
            "profile_removal_reason",
            "remove_id_images",
            "id_removal_reason",
        ]

    def validate_email(self, value):
        existing = Accounts.objects.filter(email__iexact=value)

        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise serializers.ValidationError(
                "This email address is already in use."
            )

        return value

    def validate(self, attrs):
        remove_profile = attrs.get(
            "remove_profile_picture", False
        )
        profile_reason = attrs.get(
            "profile_removal_reason", ""
        ).strip()

        selected_ids = attrs.get("remove_id_images", [])
        id_reason = attrs.get("id_removal_reason", "").strip()

        if remove_profile:
            if not self.instance.profile_picture:
                raise serializers.ValidationError({
                    "remove_profile_picture":
                        "This account has no profile picture to remove."
                })

            if not profile_reason:
                raise serializers.ValidationError({
                    "profile_removal_reason":
                        "A reason is required to remove the profile picture."
                })

        if selected_ids:
            current_images = (
                self.instance.id_images or {}
            ).get("images", [])

            if not isinstance(current_images, list):
                raise serializers.ValidationError({
                    "remove_id_images":
                        "The account's ID image data is invalid."
                })

            if len(selected_ids) != len(set(selected_ids)):
                raise serializers.ValidationError({
                    "remove_id_images":
                        "Duplicate ID image selections are not allowed."
                })

            missing_images = [
                image for image in selected_ids
                if image not in current_images
            ]

            if missing_images:
                raise serializers.ValidationError({
                    "remove_id_images":
                        "One or more selected ID images no longer exist. Refresh and try again."
                })

            if not id_reason:
                raise serializers.ValidationError({
                    "id_removal_reason":
                        "A reason is required to remove ID images."
                })

        return attrs

    def update(self, instance, validated_data):
        remove_profile = validated_data.pop(
            "remove_profile_picture", False
        )
        validated_data.pop("profile_removal_reason", None)

        selected_ids = validated_data.pop(
            "remove_id_images", []
        )
        validated_data.pop("id_removal_reason", None)

        if remove_profile:
            instance.profile_picture = None

        if selected_ids:
            id_images = instance.id_images or {}
            remaining_images = [
                image
                for image in id_images.get("images", [])
                if image not in selected_ids
            ]

            instance.id_images = {
                **id_images,
                "images": remaining_images,
            }

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance

class RoleAssignmentSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=["User", "Admin", "Super Admin"]
    )

class AccountStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()

# Review Serializers

class ReviewSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    helpful = serializers.SerializerMethodField()
    is_mine = serializers.BooleanField(read_only=True)

    class Meta:
        model = Reviews
        fields = ["id", "user", "car", "rating", "text", "status", "helpful_count", "images", "created_at", "helpful","is_mine"]

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

# Logs Serializers

class AdminActivityLogSerializer(serializers.ModelSerializer):
    admin_name = serializers.SerializerMethodField()

    class Meta:
        model = AdminActivityLog
        fields = [
            "id",
            "admin",
            "admin_name",
            "action",
            "description",
            "target_type",
            "target_id",
            "created_at",
        ]
        read_only_fields = fields

    def get_admin_name(self, obj):
        if obj.admin:
            return (
                obj.admin.get_full_name()
                or obj.admin.email
                or obj.admin.username
            )
        return "Deleted Admin"
