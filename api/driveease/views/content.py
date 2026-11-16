from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from ..models import (
    AdminActivityLog,
    FileUploadModel,
    HomePageContent,
    HomePageFAQ,
    HomePageFeaturedCar,
    HomePageTrustItem,
    AboutUs,
    AboutUsTeam,
    AboutUsWwrStats,
    AboutUsJourney,
    ContactPageContent,
    ContactOpeningHour,
    Accounts,
)
from ..serializers import (
    HomePageContentSerializer,
    HomePageFAQSerializer,
    HomePageFeaturedCarSerializer,
    HomePageTrustItemSerializer,
    AboutUsSerializer,
    AboutUsWwrStatsSerializer,
    AboutUsTeamSerializer,
    AboutUsJourneySerializer,
    ContactPageContentSerializer,
    ContactOpeningHourSerializer,
    AboutTeamUserOptionSerializer,
)
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


def delete_uploaded_file(upload_id):
    """Delete cloud storage and its upload record after a successful commit."""
    upload = FileUploadModel.objects.filter(pk=upload_id).first()
    if upload is None:
        return

    upload.file.delete(save=False)
    upload.delete()

class HomePageContentObjectMixin:
    serializer_class = HomePageContentSerializer

    def get_object(self):
        content, _ = HomePageContent.objects.get_or_create(
            pk=1,
            defaults={
                "hero_heading1": "Drive Smart",
                "hero_heading2": "Drive Easy",
                "hero_tagline": "Affordable. Reliable. Ready when you are.",
                "fleet_heading": "Find the Right Car for Your Trip",
                "fleet_description": "From budget-friendly to premium — we have it all",
                "faq_heading": "Got Questions?",
                "faq_highlight": "We've Got Answers",
                "faq_description": "Frequently asked questions about DriveEase.",
                "faq_button_label": "Ask more questions",
                "faq_button_link": "/client/contact",
            },
        )
        return content


class PublicHomePageContentView(HomePageContentObjectMixin, RetrieveAPIView):
    permission_classes = [AllowAny]

class HomePageContentUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def _prepare_children(self, content, data, key, model, serializer_class):
        if key not in data:
            return None

        items = data.get(key)
        if not isinstance(items, list):
            raise ValidationError({key: "Expected a list of items."})

        prepared = []
        submitted_ids = set()

        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValidationError({key: {index: "Expected an object."}})

            item_id = item.get("id")
            instance = None

            if item_id:
                try:
                    item_id = int(item_id)
                except (TypeError, ValueError):
                    raise ValidationError({key: {index: "Invalid item id."}})

                if item_id in submitted_ids:
                    raise ValidationError({key: {index: "Duplicate item id."}})

                instance = model.objects.filter(
                    pk=item_id,
                    homepage=content,
                ).first()
                if instance is None:
                    raise ValidationError({key: {index: "Item does not belong to this homepage."}})

                submitted_ids.add(item_id)

            payload = {
                field: value
                for field, value in item.items()
                if field != "id"
            }
            payload["order"] = index

            serializer = serializer_class(
                instance,
                data=payload,
                partial=instance is not None,
                context={"request": self.request},
            )
            serializer.is_valid(raise_exception=True)
            prepared.append(serializer)

        return prepared, submitted_ids

    @transaction.atomic
    def patch(self, request):
        content = get_object_or_404(HomePageContent, pk=1)

        trust_items = self._prepare_children(
            content,
            request.data,
            "trust_items",
            HomePageTrustItem,
            HomePageTrustItemSerializer,
        )
        featured_cars = self._prepare_children(
            content,
            request.data,
            "featured_cars",
            HomePageFeaturedCar,
            HomePageFeaturedCarSerializer,
        )
        faqs = self._prepare_children(
            content,
            request.data,
            "faqs",
            HomePageFAQ,
            HomePageFAQSerializer,
        )

        old_image_url = content.hero_image

        deleted_image = request.data.get("deleted_image")
        deleted_featured_images = request.data.get(
            "deleted_featured_images",
            [],
        )

        if not isinstance(deleted_featured_images, list):
            raise ValidationError({
                "deleted_featured_images": "Expected a list of image URLs."
            })

        # Validate against the old database state before replaced/removed rows
        # are synchronized. This prevents deleting an unrelated upload URL.
        owned_featured_images = set(
            content.featured_cars.exclude(featured_image__isnull=True)
            .exclude(featured_image="")
            .values_list("featured_image", flat=True)
        )
        requested_featured_deletions = {
            image_url
            for image_url in deleted_featured_images
            if image_url
        }
        if requested_featured_deletions - owned_featured_images:
            raise ValidationError({
                "deleted_featured_images": (
                    "One or more images do not belong to this homepage."
                )
            })

        if featured_cars is not None:
            retained_featured_images = set()
            child_serializers, _ = featured_cars
            for child_serializer in child_serializers:
                image_url = child_serializer.validated_data.get(
                    "featured_image"
                )
                if image_url is None and child_serializer.instance is not None:
                    image_url = child_serializer.instance.featured_image
                if image_url:
                    retained_featured_images.add(image_url)

            # Never delete a URL that the submitted featured list still uses.
            if requested_featured_deletions & retained_featured_images:
                raise ValidationError({
                    "deleted_featured_images": (
                        "An image selected for deletion is still in use."
                    )
                })

        # Validate the image selected for deletion.
        if deleted_image and deleted_image != old_image_url:
            return Response(
                {
                    "deleted_image": (
                        "The selected image does not belong "
                        "to the homepage content."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = HomePageContentSerializer(
            content,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        for prepared, model in (
            (trust_items, HomePageTrustItem),
            (featured_cars, HomePageFeaturedCar),
            (faqs, HomePageFAQ),
        ):
            if prepared is None:
                continue

            child_serializers, submitted_ids = prepared
            model.objects.filter(homepage=content).exclude(
                pk__in=submitted_ids
            ).delete()

            for child_serializer in child_serializers:
                if child_serializer.instance is None:
                    child_serializer.save(homepage=content)
                else:
                    child_serializer.save()

        images_to_delete = requested_featured_deletions
        if deleted_image:
            images_to_delete.add(deleted_image)

        # External storage cannot be rolled back, so cleanup runs only after
        # every homepage database change commits successfully.
        if images_to_delete:
            for upload in FileUploadModel.objects.exclude(file=""):
                if upload.file.url in images_to_delete:
                    transaction.on_commit(
                        lambda upload_id=upload.pk: delete_uploaded_file(upload_id),
                        robust=True,
                    )

        AdminActivityLog.objects.create(
            admin=request.user,
            action="update",
            description="Updated homepage content.",
            target_type="homepage_content",
            target_id=str(content.content_reference),
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class HomePageChildMixin:
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return super().get_queryset().filter(homepage_id=1)

    def perform_create(self, serializer):
        homepage = HomePageContent.objects.get(pk=1)
        serializer.save(homepage=homepage)

# Featured Cars
class FeaturedCarListCreateView(
    HomePageChildMixin,
    ListCreateAPIView,
):
    queryset = HomePageFeaturedCar.objects.select_related("car")
    serializer_class = HomePageFeaturedCarSerializer

class FeaturedCarDetailView(
    HomePageChildMixin,
    RetrieveUpdateDestroyAPIView,
):
    queryset = HomePageFeaturedCar.objects.select_related("car")
    serializer_class = HomePageFeaturedCarSerializer

# Trust Items
class TrustItemListCreateView(
    HomePageChildMixin,
    ListCreateAPIView,
):
    queryset = HomePageTrustItem.objects.all()
    serializer_class = HomePageTrustItemSerializer

class TrustItemDetailView(
    HomePageChildMixin,
    RetrieveUpdateDestroyAPIView,
):
    queryset = HomePageTrustItem.objects.all()
    serializer_class = HomePageTrustItemSerializer

# FAQs
class FAQListCreateView(
    HomePageChildMixin,
    ListCreateAPIView,
):
    queryset = HomePageFAQ.objects.all()
    serializer_class = HomePageFAQSerializer

class FAQDetailView(
    HomePageChildMixin,
    RetrieveUpdateDestroyAPIView,
):
    queryset = HomePageFAQ.objects.all()
    serializer_class = HomePageFAQSerializer

class AboutUsPageContentObjectMixin():
    serializer_class = AboutUsSerializer
    
    def get_object(self):
        content, _ = AboutUs.objects.get_or_create(
            pk=2,
            defaults={
                "wwr_heading": "Drive Smart",
                "wwr_description": "Drive Easy",
                "mission_heading": "Our Mission",
                "mission_description": "Our mission is to provide the best driving experience for our customers.",
                "vission_heading": "Our Vision",
                "vission_description": "Our vision is to be the best driving experience for our customers.",
            },
        )
        return content

class PublicAboutUsContentView(AboutUsPageContentObjectMixin, RetrieveAPIView):
    permission_classes = [AllowAny]


class AboutTeamUserOptionsView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AboutTeamUserOptionSerializer
    pagination_class = None

    def get_queryset(self):
        return Accounts.objects.filter(is_active=True).order_by(
            "first_name",
            "last_name",
            "email",
        )


class RelatedContentUpdateMixin:
    def prepare_related(
        self,
        parent,
        data,
        key,
        model,
        serializer_class,
        parent_field,
    ):
        if key not in data:
            return None

        items = data.get(key)
        if not isinstance(items, list):
            raise ValidationError({key: "Expected a list of items."})

        prepared = []
        submitted_ids = set()
        parent_filter = {parent_field: parent}

        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValidationError({key: {index: "Expected an object."}})

            item_id = item.get("id")
            instance = None
            if item_id:
                try:
                    item_id = int(item_id)
                except (TypeError, ValueError):
                    raise ValidationError({key: {index: "Invalid item id."}})

                if item_id in submitted_ids:
                    raise ValidationError({key: {index: "Duplicate item id."}})

                instance = model.objects.filter(pk=item_id, **parent_filter).first()
                if instance is None:
                    raise ValidationError({key: {index: "Item does not belong to this page."}})
                submitted_ids.add(item_id)

            payload = {field: value for field, value in item.items() if field != "id"}
            payload["order"] = index
            child_serializer = serializer_class(
                instance,
                data=payload,
                partial=instance is not None,
                context={"request": self.request},
            )
            child_serializer.is_valid(raise_exception=True)
            prepared.append(child_serializer)

        return prepared, submitted_ids

    def save_related(self, parent, prepared, model, parent_field):
        if prepared is None:
            return

        child_serializers, submitted_ids = prepared
        parent_filter = {parent_field: parent}
        model.objects.filter(**parent_filter).exclude(pk__in=submitted_ids).delete()

        for child_serializer in child_serializers:
            if child_serializer.instance is None:
                child_serializer.save(**parent_filter)
            else:
                child_serializer.save()


class AboutUsContentUpdateView(
    RelatedContentUpdateMixin,
    AboutUsPageContentObjectMixin,
    APIView,
):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def patch(self, request):
        content = self.get_object()
        old_image_url = content.wwr_image
        deleted_image = request.data.get("deleted_image")

        if deleted_image and deleted_image != old_image_url:
            raise ValidationError({
                "deleted_image": (
                    "The selected image does not belong to the About content."
                )
            })

        related = (
            ("wwr_stats", AboutUsWwrStats, AboutUsWwrStatsSerializer),
            ("team", AboutUsTeam, AboutUsTeamSerializer),
            ("journey", AboutUsJourney, AboutUsJourneySerializer),
        )
        prepared = [
            (
                self.prepare_related(
                    content,
                    request.data,
                    key,
                    model,
                    serializer_class,
                    "about_us",
                ),
                model,
            )
            for key, model, serializer_class in related
        ]

        serializer = AboutUsSerializer(content, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        for child_data, model in prepared:
            self.save_related(content, child_data, model, "about_us")

        # Cloud deletion is irreversible, so only run it once every database
        # change in this atomic update has committed successfully.
        if deleted_image:
            for upload in FileUploadModel.objects.exclude(file=""):
                if upload.file.url == deleted_image:
                    transaction.on_commit(
                        lambda upload_id=upload.pk: delete_uploaded_file(upload_id),
                        robust=True,
                    )
                    break

        AdminActivityLog.objects.create(
            admin=request.user,
            action="update",
            description="Updated About page content.",
            target_type="about_content",
            target_id=str(content.content_reference),
        )
        return Response(AboutUsSerializer(content).data)


class ContactPageContentObjectMixin:
    serializer_class = ContactPageContentSerializer

    def get_object(self):
        content, created = ContactPageContent.objects.get_or_create(
            pk=1,
            defaults={
                "form_description": "Fill out the form and our team will get back to you within 24 hours.",
                "phone": "0960 064 4095",
                "email": "driveease.biz@gmail.com",
                "address": "Tipolo, Mandaue City, Philippines, 6014",
            },
        )
        if created:
            ContactOpeningHour.objects.bulk_create([
                ContactOpeningHour(
                    contact_page=content,
                    day="Monday - Friday",
                    time="8:00 AM - 6:00 PM",
                    order=0,
                ),
                ContactOpeningHour(
                    contact_page=content,
                    day="Saturday",
                    time="9:00 AM - 5:00 PM",
                    order=1,
                ),
                ContactOpeningHour(
                    contact_page=content,
                    day="Sunday",
                    time="Closed",
                    is_closed=True,
                    order=2,
                ),
            ])
        return content


class PublicContactPageContentView(ContactPageContentObjectMixin, RetrieveAPIView):
    permission_classes = [AllowAny]


class ContactPageContentUpdateView(
    RelatedContentUpdateMixin,
    ContactPageContentObjectMixin,
    APIView,
):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def patch(self, request):
        content = self.get_object()
        opening_hours = self.prepare_related(
            content,
            request.data,
            "opening_hours",
            ContactOpeningHour,
            ContactOpeningHourSerializer,
            "contact_page",
        )

        serializer = ContactPageContentSerializer(
            content,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.save_related(
            content,
            opening_hours,
            ContactOpeningHour,
            "contact_page",
        )

        AdminActivityLog.objects.create(
            admin=request.user,
            action="update",
            description="Updated Contact page content.",
            target_type="contact_content",
            target_id=str(content.content_reference),
        )
        return Response(ContactPageContentSerializer(content).data)
