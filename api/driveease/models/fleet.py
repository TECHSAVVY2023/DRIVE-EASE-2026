from django.conf import settings
from django.db import models
from django.utils.text import slugify

from . import default_car_meta, generate_car_reference


class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Feature"
        verbose_name_plural = "Features"

    def save(self, *args, **kwargs):
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
    CAR_STATUS = [('available', 'Available'), ('maintenance', 'Maintenance')]

    car_reference = models.CharField(
        max_length=30, unique=True, default=generate_car_reference, editable=False
    )
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    car_type = models.ForeignKey(CarType, on_delete=models.PROTECT, related_name="cars")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    transmission = models.CharField(max_length=50)
    engine = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=50)
    seats = models.IntegerField()
    features = models.ManyToManyField("Feature", blank=True, related_name="cars")
    note = models.TextField(blank=True, null=True)
    meta = models.JSONField(default=default_car_meta, blank=True)
    status = models.CharField(max_length=20, choices=CAR_STATUS, default='available')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.car_reference})"
