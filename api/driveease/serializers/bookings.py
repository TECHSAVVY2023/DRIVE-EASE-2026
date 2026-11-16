from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Accounts, Booking, Cars, Payment, Refund

User = get_user_model()


class BookingSerializer(serializers.ModelSerializer):
    user_reference = serializers.SlugRelatedField(
        source="user", slug_field="user_reference", queryset=Accounts.objects.all(), write_only=True
    )
    car_reference = serializers.SlugRelatedField(
        source="car", slug_field="car_reference", queryset=Cars.objects.all(), write_only=True
    )

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['booking_reference', 'created_at', 'updated_at']
        extra_kwargs = {'user': {'read_only': True}, 'car': {'read_only': True}}


class TransactionCarSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Cars
        fields = ("car_reference", "brand", "model", "image", "year")

    def get_image(self, obj):
        return obj.meta.get("primary_image")


class TransactionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "user_reference", "email", "first_name", "last_name",
            "contact_number", "address", "id_images", "profile_picture"
        )


class TransactionSerializer(serializers.ModelSerializer):
    car = TransactionCarSerializer(read_only=True)
    user = TransactionUserSerializer(read_only=True)
    payment_method = serializers.CharField(source="payments.payment_method", read_only=True)
    payment_status = serializers.CharField(source="payments.status", read_only=True)
    refund = serializers.SerializerMethodField()
    can_refund = serializers.SerializerMethodField()
    refund_unavailable_reason = serializers.SerializerMethodField()

    def _payment(self, obj):
        try:
            return obj.payments
        except Payment.DoesNotExist:
            return None

    def get_refund(self, obj):
        payment = self._payment(obj)
        if not payment:
            return None

        refund = payment.refunds.order_by("-requested_at").first()
        return RefundSerializer(refund).data if refund else None

    def get_can_refund(self, obj):
        payment = self._payment(obj)
        if not payment or obj.status not in {"cancelled", "rejected"}:
            return False
        if payment.status != "paid" or not payment.paymongo_payment_id:
            return False
        return not payment.refunds.filter(status__in={"processing", "succeeded"}).exists()

    def get_refund_unavailable_reason(self, obj):
        payment = self._payment(obj)
        if not payment or obj.status not in {"cancelled", "rejected"}:
            return None
        if payment.status == "refunded":
            return "This payment has already been refunded."
        if payment.status != "paid":
            return "Only paid bookings can be refunded."
        if not payment.paymongo_payment_id:
            return "This payment was not processed through PayMongo and must be refunded manually."
        if payment.refunds.filter(status="processing").exists():
            return "The refund is currently being processed."
        if payment.refunds.filter(status="succeeded").exists():
            return "This payment has already been refunded."
        return None

    class Meta:
        model = Booking
        fields = (
            "booking_reference", "status", "car", "user", "payment_status",
            "payment_method", "created_at", "pending_approval_at", "confirmed_at",
            "picked_up_at", "returned_at", "completed_at", "cancelled_at",
            "cancel_reason", "daily_rate", "number_of_days", "subtotal", "discount",
            "total_price", "pickup_date", "return_date", "pickup_location", "return_location",
            "refund", "can_refund", "refund_unavailable_reason",
        )


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = (
            "id", "paymongo_refund_id", "amount", "reason", "customer_reason",
            "admin_note", "status", "failure_message", "requested_at",
            "processed_at", "updated_at",
        )
        read_only_fields = fields


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
