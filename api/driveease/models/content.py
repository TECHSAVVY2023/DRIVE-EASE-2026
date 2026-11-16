from django.db import models
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

from .fleet import Cars
from . import generate_content_reference

class HomePageContent(models.Model):
    content_reference = models.CharField(max_length=30, unique=True, default=generate_content_reference, editable=False)
    hero_heading1 = models.CharField(max_length=150)
    hero_heading2 = models.CharField(max_length=150)
    hero_tagline = models.CharField(max_length=255)
    hero_image = models.URLField(blank=True, null=True)
    fleet_heading = models.CharField(max_length=150)
    fleet_description = models.CharField(max_length=255)
    trust_heading = models.CharField(max_length=150, default="Why Choose Us?")
    faq_heading = models.CharField(max_length=150)
    faq_highlight = models.CharField(max_length=150, blank=True)
    faq_description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Homepage content"


class HomePageTrustItem(models.Model):
    homepage = models.ForeignKey(
        HomePageContent, on_delete=models.CASCADE, related_name="trust_items"
    )
    value = models.CharField(max_length=30)
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class HomePageFeaturedCar(models.Model):
    homepage = models.ForeignKey(
        HomePageContent,
        on_delete=models.CASCADE,
        related_name="featured_cars",
    )

    car = models.ForeignKey(
        Cars,
        on_delete=models.CASCADE,
        related_name="homepage_features",
    )
    featured_image = models.URLField(blank=True, null=True)

    order = models.PositiveIntegerField(default=0)


class HomePageFAQ(models.Model):
    homepage = models.ForeignKey(HomePageContent, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

class AboutUs(models.Model):
    content_reference = models.CharField(max_length=30, unique=True, default=generate_content_reference, editable=False)
    wwr_heading = models.CharField(max_length=150)
    wwr_description = models.TextField()
    wwr_image = models.URLField(blank=True, null=True)
    mission_heading = models.CharField(max_length=150)
    mission_description = models.TextField()
    vission_heading = models.CharField(max_length=150)
    vission_description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "About us content"

class AboutUsWwrStats(models.Model):
    about_us = models.ForeignKey(AboutUs, on_delete=models.CASCADE, related_name="wwr_stats")
    stat = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.stat} - {self.value}"

class AboutUsTeam(models.Model):
    about_us = models.ForeignKey(AboutUs, on_delete=models.CASCADE, related_name="team")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="about_us_team",
        blank=True,
        null=True,
    )
    position = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

class AboutUsJourney(models.Model):
    about_us = models.ForeignKey(AboutUs, on_delete=models.CASCADE, related_name="journey")
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class ContactPageContent(models.Model):
    content_reference = models.CharField(
        max_length=30,
        unique=True,
        default=generate_content_reference,
        editable=False,
    )
    form_heading = models.CharField(max_length=150, default="How can we help you?")
    form_description = models.TextField(blank=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    x_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Contact page content"


class ContactOpeningHour(models.Model):
    contact_page = models.ForeignKey(
        ContactPageContent,
        on_delete=models.CASCADE,
        related_name="opening_hours",
    )
    day = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    is_closed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

