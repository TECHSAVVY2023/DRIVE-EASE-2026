from rest_framework import serializers

from ..models import (
    HomePageContent,
    HomePageFAQ,
    HomePageFeaturedCar,
    HomePageTrustItem,
    AboutUs,
    AboutUsWwrStats,
    AboutUsTeam,
    AboutUsJourney,
    ContactPageContent,
    ContactOpeningHour,
    Accounts,
    Cars,
)

from .fleet import MiniCarSerializer


class HomePageFeaturedCarSerializer(serializers.ModelSerializer):
    car_name = serializers.SerializerMethodField()
    car_reference = serializers.SerializerMethodField()
    price_per_day = serializers.DecimalField(
        source="car.price_per_day",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = HomePageFeaturedCar
        fields = [
            "id",
            "car",
            "car_name",
            "car_reference",
            "price_per_day",
            "featured_image",
            "order",
        ]
        read_only_fields = ["id", "car_name", "car_reference", "price_per_day"]

    def get_car_name(self, obj):
        return f"{obj.car.brand} {obj.car.model} {obj.car.year}"

    def get_car_reference(self, obj):
        return obj.car.car_reference

class HomePageTrustItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageTrustItem
        fields = ["id", "value", "label", "order"]
        read_only_fields = ["id"]


class HomePageFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageFAQ
        fields = [
            "id",
            "question",
            "answer",
            "order",
        ]
        read_only_fields = ["id"]
    
class AboutUsJourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsJourney
        fields = [
            "id",
            "title",
            "description",
            "year",
            "order",
        ]
        read_only_fields = ["id"]

class AboutUsTeamSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=Accounts.objects.filter(is_active=True),
        allow_null=False,
        required=True,
    )
    user_name = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_profile_picture = serializers.URLField(
        source="user.profile_picture",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = AboutUsTeam
        fields = [
            "id",
            "user",
            "user_name",
            "user_email",
            "user_profile_picture",
            "position",
            "description",
            "order",
        ]
        read_only_fields = ["id"]

    def get_user_name(self, obj):
        if obj.user is None:
            return "Deleted User"
        return obj.user.get_full_name() or obj.user.email or obj.user.username


class AboutTeamUserOptionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Accounts
        fields = ["id", "user_reference", "name", "email", "profile_picture"]

    def get_name(self, obj):
        return obj.get_full_name() or obj.email or obj.username

class AboutUsWwrStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsWwrStats
        fields = [
            "id",
            "stat",
            "value",
            "order",
        ]
        read_only_fields = ["id"]

class AboutUsSerializer(serializers.ModelSerializer):
    wwr_stats = AboutUsWwrStatsSerializer(many=True, read_only=True)
    team = AboutUsTeamSerializer(many=True, read_only=True)
    journey = AboutUsJourneySerializer(many=True, read_only=True)

    class Meta:
        model = AboutUs
        fields = [
            "id",
            "content_reference",
            "wwr_heading",
            "wwr_description",
            "wwr_image",
            "wwr_stats",
            "mission_heading",
            "mission_description",
            "vission_heading",
            "vission_description",
            "team",
            "journey",
            "updated_at",
        ]
        read_only_fields = ["id"]


class ContactOpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactOpeningHour
        fields = ["id", "day", "time", "is_closed", "order"]
        read_only_fields = ["id"]


class ContactPageContentSerializer(serializers.ModelSerializer):
    opening_hours = ContactOpeningHourSerializer(many=True, read_only=True)

    class Meta:
        model = ContactPageContent
        fields = [
            "id",
            "content_reference",
            "form_heading",
            "form_description",
            "phone",
            "email",
            "address",
            "facebook_url",
            "instagram_url",
            "x_url",
            "tiktok_url",
            "opening_hours",
            "updated_at",
        ]
        read_only_fields = ["id", "content_reference", "updated_at"]


class HomePageContentSerializer(serializers.ModelSerializer):
    featured_cars = HomePageFeaturedCarSerializer(many=True, read_only=True)
    trust_items = HomePageTrustItemSerializer(many=True, read_only=True)
    faqs = HomePageFAQSerializer(many=True, read_only=True)
    cars = serializers.SerializerMethodField()

    def get_cars(self, obj):
        return MiniCarSerializer(
            Cars.objects.all(),
            many=True,
            context=self.context
        ).data

    class Meta:
        model = HomePageContent
        fields = [
            "id",
            "content_reference",
            "hero_heading1",
            "hero_heading2",
            "hero_tagline",
            "hero_image",
            "fleet_heading",
            "fleet_description",
            "trust_heading",
            "trust_items",
            "faq_heading",
            "faq_highlight",
            "faq_description",
            "featured_cars",
            "faqs",
            "cars",
            "updated_at",
        ]
