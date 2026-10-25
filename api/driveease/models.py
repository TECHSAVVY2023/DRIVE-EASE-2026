import os
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from storages.backends.s3boto3 import S3Boto3Storage
from django.utils.text import slugify


def unique_upload_path(instance, filename):
    """Give every uploaded file its own immutable storage key."""
    extension = os.path.splitext(filename)[1].lower()
    return f"app/uploads/{uuid.uuid4().hex}{extension}"

def default_car_meta():
    return {
        "primary_image": "",
        "images": []
    }

def default_user_id():
    return {
        "images": []
    }

class Feature(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        max_length=100,
        blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Feature"
        verbose_name_plural = "Features"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CarType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Cars(models.Model):

    CAR_STATUS = [
        ('available', 'Available'),
        ('maintenance', 'Maintenance'),
    ]

    car_id = models.CharField(
        max_length=50,
        primary_key=True
    )

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()

    car_type = models.ForeignKey(
        CarType,
        on_delete=models.PROTECT,
        related_name="cars",
    )

    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    transmission = models.CharField(max_length=50)
    engine = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=50)

    seats = models.IntegerField()

    features = models.ManyToManyField(
        "Feature",
        blank=True,
        related_name="cars"
    )

    note = models.TextField(blank=True, null=True)

    meta = models.JSONField(default=default_car_meta, blank=True)

    status = models.CharField(
        max_length=20,
        choices=CAR_STATUS,
        default='available'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    approval_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.car_id})"

class Accounts(AbstractUser):
    contact_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    profile_picture = models.URLField(blank=True, null=True)
    id_images = models.JSONField(default=default_user_id, blank=True)

    def __str__(self):
        return self.username

class Reviews(models.Model):

    REVIEW_STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("hidden", "Hidden"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    car = models.ForeignKey(
        'Cars',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField()

    text = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=REVIEW_STATUS,
        default="pending"
    )

    helpful_count = models.PositiveIntegerField(default=0)

    images = models.JSONField(
        default=list,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ('user', 'car')

    def __str__(self):
        return f'{self.user} - {self.car}'

class ReviewHelpful(models.Model):
    review = models.ForeignKey(
        "Reviews",
        on_delete=models.CASCADE,
        related_name="helpful_votes"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="helpful_reviews"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review Helpful"
        verbose_name_plural = "Review Helpful"
        constraints = [
            models.UniqueConstraint(
                fields=["review", "user"],
                name="unique_review_helpful_vote"
            )
        ]

class FileUploadModel(models.Model):

    file = models.FileField(
        storage=S3Boto3Storage(),
        upload_to=unique_upload_path,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class ContactListModel(models.Model):
    contact_id = models.CharField(max_length=255, blank=True, null=True, default='')
    firstname = models.CharField(max_length=255, blank=True, null=True, default='')
    lastname = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_email = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_number = models.CharField(max_length=255, blank=True, null=True, default='')
    message = models.CharField(max_length=500, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
  
    class Meta: 
        ordering = ('-created_at',)

    def created_at_formatted(self):
        return defaultfilters.date(self.created_at, 'M d, Y')

class Booking(models.Model):
    BOOKING_STATUS = [
        ("pending_payment", "Pending Payment"),
        ("pending_approval", "Pending Approval"),
        ("confirmed", "Confirmed"),
        ("rejected", "Rejected"),
        ("picked_up", "Picked Up"),
        ("returned", "Returned"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    car = models.ForeignKey(
        'Cars',
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    booking_reference = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    pickup_date = models.DateTimeField()
    return_date = models.DateTimeField()
    
    pickup_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    return_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    # Pricing Snapshot
    daily_rate = models.DecimalField(max_digits=10,decimal_places=2)
    number_of_days = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default='pending_payment'
    )

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
        from django.utils import timezone
        import uuid

        changed_fields = set()

        if not self.booking_reference:
            self.booking_reference = f"BKG-{uuid.uuid4().hex[:10].upper()}"
            changed_fields.add("booking_reference")

        milestone_fields = {
            "pending_approval": ("pending_approval_at",),
            "confirmed": (
                "pending_approval_at",
                "confirmed_at",
            ),
            "picked_up": (
                "pending_approval_at",
                "confirmed_at",
                "picked_up_at",
            ),
            "returned": (
                "pending_approval_at",
                "confirmed_at",
                "picked_up_at",
                "returned_at",
            ),
            "completed": (
                "pending_approval_at",
                "confirmed_at",
                "picked_up_at",
                "returned_at",
                "completed_at",
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

        # Ensure automatically populated milestones are persisted even when
        # the caller saves only a restricted set of fields.
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
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    checkout_session_id = models.CharField(max_length=255,unique=True)
    payment_intent_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='PHP')
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    payment_method = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    paymongo_response = models.JSONField(default=dict, blank=True)

    paid_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.booking.booking_reference} - {self.amount} {self.currency} ({self.status})'

class Notification(models.Model):

    class NotificationType(models.TextChoices):
        BOOKING = "booking", "Booking"
        PAYMENT = "payment", "Payment"
        REMINDER = "reminder", "Reminder"
        SYSTEM = "system", "System"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    # Frontend route/page to open when notification is clicked
    action_url = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    # Optional references to related objects
    booking = models.ForeignKey(
        "Booking",
        on_delete=models.CASCADE,
        related_name="notifications",
        blank=True,
        null=True,
    )

    is_read = models.BooleanField(default=False)

    read_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_read"]),
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.title}"

class AdminActivityLog(models.Model):
    ACTION_CHOICES = [
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("status_change", "Status Change"),
    ]

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="activity_logs",
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
    )

    description = models.TextField()

    target_type = models.CharField(
        max_length=50,
    )

    target_id = models.CharField(
        max_length=100,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.admin} - {self.action} - {self.target_type}"
