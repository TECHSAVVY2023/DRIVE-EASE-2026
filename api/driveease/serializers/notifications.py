from rest_framework import serializers

from ..models import Booking, Notification


class NotificationBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["booking_reference", "status"]


class NotificationSerializer(serializers.ModelSerializer):
    booking = NotificationBookingSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id", "notification_type", "title", "message", "action_url",
            "booking", "is_read", "read_at", "created_at",
        ]
        read_only_fields = fields
