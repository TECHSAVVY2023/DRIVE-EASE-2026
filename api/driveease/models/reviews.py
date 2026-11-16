from django.conf import settings
from django.db import models

from . import generate_review_reference


class Reviews(models.Model):
    REVIEW_STATUS = [("pending", "Pending"), ("approved", "Approved"), ("hidden", "Hidden")]

    review_reference = models.CharField(
        max_length=30, unique=True, default=generate_review_reference, editable=False
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    car = models.ForeignKey('Cars', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    status = models.CharField(max_length=10, choices=REVIEW_STATUS, default="pending")
    helpful_count = models.PositiveIntegerField(default=0)
    images = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ('user', 'car')

    def __str__(self):
        return f'{self.user} - {self.car}'


class ReviewHelpful(models.Model):
    review = models.ForeignKey("Reviews", on_delete=models.CASCADE, related_name="helpful_votes")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="helpful_reviews"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review Helpful"
        verbose_name_plural = "Review Helpful"
        constraints = [
            models.UniqueConstraint(fields=["review", "user"], name="unique_review_helpful_vote")
        ]
