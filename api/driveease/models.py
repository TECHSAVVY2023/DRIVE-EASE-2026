from django.db import models
from django.template import defaultfilters
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage

def default_car_meta():
    return {
        "primary_image": "",
        "images": []
    }
def default_user_id():
    return {
        "images": []
    }

# Create your models here.
class Cars(models.Model):

    CAR_STATUS = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Maintenance'),
    ]

    CAR_TYPE = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('hatchback', 'Hatchback'),
        ('pickup', 'Pickup'),
        ('other', 'Other'),
    ]

    car_id = models.CharField(
        max_length=50,
        primary_key=True
    )

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()

    car_type = models.CharField(
        max_length=50,
        choices=CAR_TYPE,
        default='other'
    )

    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    transmission = models.CharField(max_length=50)
    engine = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=50)

    seats = models.IntegerField()

    features = models.JSONField(default=list, blank=True)

    note = models.TextField(blank=True, null=True)

    meta = models.JSONField(default=default_car_meta, blank=True)

    status = models.CharField(
        max_length=20,
        choices=CAR_STATUS,
        default='available'
    )

    created_by = models.ForeignKey(
        User,
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

class FileUploadModel(models.Model):

    file = models.FileField(storage=S3Boto3Storage(), upload_to='app/fleet/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    contact_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    profile_picture = models.URLField(blank=True, null=True)
    id_images = models.JSONField(default=default_user_id, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"

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