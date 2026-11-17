from rest_framework import serializers
from django.utils import timezone

from ..models import Cars, CarType, Feature
from ..utils.booking_availability import booking_blocks_availability


class MiniCarSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Cars
        # The content editor needs the numeric id for the featured-car FK.
        fields = (
            "id",
            "car_reference",
            "brand",
            "model",
            "image",
            "year",
            "price_per_day",
        )

    def get_image(self, obj):
        return obj.meta.get("primary_image")


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = ["id", "name", "slug"]


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "name", "slug"]


class CarSerializer(serializers.ModelSerializer):
    unavailable_periods = serializers.SerializerMethodField()
    rental_count = serializers.IntegerField(read_only=True)
    car_type = serializers.SlugRelatedField(read_only=True, slug_field="slug")
    features = serializers.SlugRelatedField(many=True, read_only=True, slug_field="slug")

    class Meta:
        model = Cars
        fields = "__all__"

    def get_unavailable_periods(self, obj):
        bookings = obj.bookings.filter(booking_blocks_availability())
        now = timezone.now()
        return [
            {
                "pickup_date": booking.pickup_date,
                "return_date": booking.return_date,
                "status": booking.status,
                "is_overdue": (
                    booking.status in {
                        "pending_approval",
                        "confirmed",
                        "picked_up",
                    }
                    and booking.pickup_date <= now
                    and booking.return_date <= now
                ),
            }
            for booking in bookings
        ]


class CarCreateSerializer(serializers.ModelSerializer):
    car_type = serializers.SlugRelatedField(
        slug_field="slug", queryset=CarType.objects.all(), allow_null=True
    )
    features = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Feature.objects.all()
    )

    class Meta:
        model = Cars
        fields = [
            "car_reference", "brand", "model", "year", "car_type",
            "price_per_day", "transmission", "engine", "fuel_type",
            "seats", "note", "meta", "status", "features",
        ]
        read_only_fields = ["car_reference"]

    def create(self, validated_data):
        features = validated_data.pop("features", [])
        validated_data["created_by"] = self.context["request"].user
        car = Cars.objects.create(**validated_data)
        car.features.set(features)
        return car


class CarUpdateSerializer(serializers.ModelSerializer):
    car_type = serializers.SlugRelatedField(
        slug_field="slug", queryset=CarType.objects.all(), allow_null=True
    )
    features = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Feature.objects.all()
    )

    class Meta:
        model = Cars
        fields = [
            "car_reference", "brand", "model", "year", "car_type",
            "price_per_day", "transmission", "engine", "fuel_type",
            "seats", "note", "meta", "status", "features",
        ]
        read_only_fields = ["car_reference"]
