from rest_framework import serializers

from ..models import Reviews
from .common import UserMiniSerializer
from .fleet import MiniCarSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    helpful = serializers.SerializerMethodField()
    is_mine = serializers.BooleanField(read_only=True)

    class Meta:
        model = Reviews
        fields = [
            "id", "review_reference", "user", "car", "rating", "text",
            "status", "helpful_count", "images", "created_at", "helpful", "is_mine",
        ]

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
            'id', 'review_reference', 'car', 'user', 'rating', 'text',
            'status', 'created_at', 'images', 'helpful_count',
        ]
