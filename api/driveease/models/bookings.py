from django.conf import settings
from django.db import models
from django.utils import timezone

from . import generate_booking_reference


class Booking(models.Model):
    BOOKING_STATUS = [
        ("pending_payment", "Pending Payment"), ("payment_failed", "Payment Failed"),
        ("pending_approval", "Pending Approval"),
        ("confirmed", "Confirmed"), ("rejected", "Rejected"),
        ("picked_up", "Picked Up"), ("returned", "Returned"),
        ("completed", "Completed"), ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey('Cars', on_delete=models.CASCADE, related_name='bookings')
    booking_reference = models.CharField(
        max_length=30, unique=True, default=generate_booking_reference, editable=False
    )
    pickup_date = models.DateTimeField()
    return_date = models.DateTimeField()
    pickup_location = models.CharField(max_length=255, blank=True, null=True)
    return_location = models.CharField(max_length=255, blank=True, null=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_days = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending_payment')
    pending_approval_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancel_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        changed_fields = set()
        milestone_fields = {
            "pending_approval": ("pending_approval_at",),
            "confirmed": ("pending_approval_at", "confirmed_at"),
            "picked_up": ("pending_approval_at", "confirmed_at", "picked_up_at"),
            "returned": ("pending_approval_at", "confirmed_at", "picked_up_at", "returned_at"),
            "completed": (
                "pending_approval_at", "confirmed_at", "picked_up_at", "returned_at", "completed_at"
            ),
        }
        transition_time = timezone.now()

        for field_name in milestone_fields.get(self.status, ()):
            if getattr(self, field_name) is None:
                setattr(self, field_name, transition_time)
                changed_fields.add(field_name)

        if self.status == "cancelled" and self.cancelled_at is None:
            self.cancelled_at = transition_time
            changed_fields.add("cancelled_at")

        if kwargs.get("update_fields") is not None:
            kwargs["update_fields"] = set(kwargs["update_fields"]) | changed_fields
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user.username} - {self.car.brand} {self.car.model} ({self.pickup_date})'


class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'), ('paid', 'Paid'),
        ('failed', 'Failed'), ('refunded', 'Refunded'),
    ]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payments')
    checkout_session_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    payment_intent_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    paymongo_payment_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='PHP')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    paymongo_response = models.JSONField(default=dict, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.booking.booking_reference} - {self.amount} {self.currency} ({self.status})'


class Refund(models.Model):
    REFUND_STATUS = [
        ('pending_review', 'Pending Review'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('rejected', 'Rejected'),
    ]

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    paymongo_refund_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=50, default='customer_cancellation')
    customer_reason = models.TextField(blank=True)
    admin_note = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=REFUND_STATUS, default='pending_review')
    failure_message = models.TextField(blank=True)
    paymongo_response = models.JSONField(default=dict, blank=True)
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requested_refunds',
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_refunds',
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-requested_at',)

    def __str__(self):
        return f'{self.payment.booking.booking_reference} - {self.amount} ({self.status})'
