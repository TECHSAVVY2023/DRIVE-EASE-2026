from django.conf import settings
from django.db import models


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        BOOKING = "booking", "Booking"
        BOOKING_STATUS = "booking_status", "Booking Status"
        PAYMENT = "payment", "Payment"
        REVIEW = "review", "Review"
        REMINDER = "reminder", "Reminder"
        SYSTEM = "system", "System"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    action_url = models.CharField(max_length=500, blank=True, null=True)
    booking = models.ForeignKey(
        "Booking", on_delete=models.CASCADE, related_name="notifications", blank=True, null=True
    )
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deduplication_key = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_read"]),
            models.Index(fields=["user", "-created_at"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "deduplication_key"],
                condition=models.Q(deduplication_key__isnull=False),
                name="unique_notification_recipient_event",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.title}"


class CarAvailabilityAlert(models.Model):
    """A one-time request to notify a customer when a rented car is free."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="car_availability_alerts",
    )
    car = models.ForeignKey(
        "Cars",
        on_delete=models.CASCADE,
        related_name="availability_alerts",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "car"],
                name="unique_user_car_availability_alert",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.car} availability"
