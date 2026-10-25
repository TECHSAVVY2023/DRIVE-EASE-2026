"""Reviews API views."""

from django.db import transaction
from django.db.models import Avg, BooleanField, Case, Count, F, Q, Value, When
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import AdminActivityLog, Cars, FileUploadModel, ReviewHelpful, Reviews
from ..pagination import AdminReviewPagination, ReviewPagination
from ..serializers import AdminReviewSerializer, ReviewSerializer


def delete_review_uploads_from_storage(urls):
    """Delete review files managed through FileUploadModel."""
    urls_to_delete = {url for url in urls if url}

    if not urls_to_delete:
        return

    for upload in FileUploadModel.objects.exclude(file=""):
        if upload.file.url not in urls_to_delete:
            continue

        upload.file.delete(save=False)
        upload.delete()


class ReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

    def get_queryset(self):
        queryset = Reviews.objects.filter(
            status="approved"
        )

        rating = self.request.query_params.get("rating")
        if rating:
            queryset = queryset.filter(rating=rating)

        sort = self.request.query_params.get("sort")

        if sort == "highest":
            queryset = queryset.order_by("-helpful_count")
        elif sort == "lowest":
            queryset = queryset.order_by("helpful_count")
        elif sort == "newest":
            queryset = queryset.order_by("-created_at")
        else:
            queryset = queryset.order_by("created_at")

        return queryset

    def list(self, request, *args, **kwargs):
        # Statistics based only on approved reviews
        stats_queryset = Reviews.objects.filter(
            status="approved"
        )

        # Filtered queryset for displayed reviews
        queryset = self.get_queryset()

        avg_rating = stats_queryset.aggregate(
            avg_rating=Avg("rating")
        )["avg_rating"] or 0

        total_reviews = stats_queryset.count()

        rating_breakdown = {
            star: stats_queryset.filter(rating=star).count()
            for star in range(1, 6)
        }

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            response.data["avg_rating"] = round(avg_rating, 1)
            response.data["rating_breakdown"] = rating_breakdown
            response.data["total_reviews"] = total_reviews

            return response


class CarReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

    def get_queryset(self):
        queryset = Reviews.objects.filter(
            car_id=self.kwargs["car_id"],
            status="approved"
        )

        # Pin the current user's review
        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                is_mine=Case(
                    When(user=self.request.user, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
        else:
            queryset = queryset.annotate(
                is_mine=Value(False, output_field=BooleanField())
            )
        
        # Filter by rating
        rating = self.request.query_params.get("rating")
        if rating:
            queryset = queryset.filter(rating=rating)

        # Sort
        sort = self.request.query_params.get("sort")

        if sort == "highest":
            queryset = queryset.order_by("-helpful_count")
        elif sort == "lowest":
            queryset = queryset.order_by("helpful_count")
        elif sort == "newest":
            queryset = queryset.order_by("-created_at")
        else:
            queryset = queryset.order_by("created_at")

        return queryset

    def list(self, request, *args, **kwargs):
        all_reviews = Reviews.objects.filter(
            car_id=self.kwargs["car_id"],
            status="approved"
        )

        queryset = self.get_queryset()

        avg_rating = all_reviews.aggregate(
            avg_rating=Avg("rating")
        )["avg_rating"] or 0

        total_reviews = all_reviews.count()

        breakdown = {
            star: all_reviews.filter(rating=star).count()
            for star in range(1, 6)
        }

        my_review = None

        if request.user.is_authenticated:
            my_review = Reviews.objects.filter(
                car_id=self.kwargs["car_id"],
                user=request.user,
            ).first()

            # Remove the user's review from the public list if present
            if my_review:
                queryset = queryset.exclude(pk=my_review.pk)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            response = self.get_paginated_response(serializer.data)

            response.data["my_review"] = (
                self.get_serializer(my_review).data
                if my_review
                else None
            )

            response.data["total_reviews"] = total_reviews
            response.data["avg_rating"] = round(avg_rating, 1)
            response.data["rating_breakdown"] = breakdown

            return response

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "results": serializer.data,
            "my_review": (
                self.get_serializer(my_review).data
                if my_review
                else None
            ),
            "total_reviews": total_reviews,
            "avg_rating": round(avg_rating, 1),
            "rating_breakdown": breakdown,
        })


class FeaturedReviewsView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return (
            Reviews.objects
            .filter(images__isnull=False)
            .order_by("-helpful_count", "?")[:3]
        )

    def list(self, request, *args, **kwargs):
        stats_queryset = Reviews.objects.all()
        queryset = self.get_queryset()

        avg_rating = stats_queryset.aggregate(
            avg_rating=Avg("rating")
        )["avg_rating"] or 0

        total_reviews = stats_queryset.count()

        rating_breakdown = {
            star: stats_queryset.filter(rating=star).count()
            for star in range(1, 6)
        }

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            response.data["avg_rating"] = round(avg_rating, 1)
            response.data["rating_breakdown"] = rating_breakdown
            response.data["total_reviews"] = total_reviews

            return response

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "results": serializer.data,
            "avg_rating": round(avg_rating, 1),
            "rating_breakdown": rating_breakdown,
            "total_reviews": total_reviews,
        })


class CreateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, car_id):
        car = Cars.objects.get(car_id=car_id)

        # Prevent duplicate reviews
        if Reviews.objects.filter(
            user=request.user,
            car=car
        ).exists():
            return Response(
                {"detail": "You have already reviewed this car."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rating = request.data.get("rating")
        text = request.data.get("comment")
        images = request.data.get("images") or []

        review = Reviews.objects.create(
            user=request.user,
            car=car,
            rating=rating,
            text=text,
            images=images,
        )

        return Response(
            {
                "message": "Review submitted successfully.",
                "review_id": review.id
            },
            status=status.HTTP_201_CREATED,
        )


class UpdateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request, car_id, review_id):
        try:
            review = Reviews.objects.get(
                id=review_id,
                user=request.user,
                car=car_id
            )
        except Reviews.DoesNotExist:
            return Response(
                {"detail": "Review not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data

        deleted_images = data.get("deleted_images", [])
        updated_images = data.get("images", review.images)

        if not isinstance(deleted_images, list):
            return Response(
                {"deleted_images": "Expected a list of URLs."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(updated_images, list):
            return Response(
                {"images": "Expected a list of URLs."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        original_images = set(review.images or [])
        invalid_urls = [
            url for url in deleted_images
            if url not in original_images
        ]

        if invalid_urls:
            return Response(
                {
                    "deleted_images": (
                        "One or more selected images do not belong "
                        "to this review."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        conflicting_urls = set(deleted_images).intersection(updated_images)

        if conflicting_urls:
            return Response(
                {
                    "deleted_images": (
                        "An image cannot be kept and deleted in the "
                        "same request."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        review.rating = data.get("rating", review.rating)
        review.text = data.get("review", review.text)
        review.images = updated_images

        review.save()
        delete_review_uploads_from_storage(deleted_images)

        return Response(
            {
                "message": "Review updated successfully.",
                "review_id": review.id,
            },
            status=status.HTTP_200_OK,
        )


class DeleteReviewView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request, car_id, review_id):
        try:
            review = Reviews.objects.get(
                id=review_id,
                user=request.user,
                car=car_id
            )
        except Reviews.DoesNotExist:
            return Response(
                {"detail": "Review not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        delete_review_uploads_from_storage(review.images or [])
        review.delete()

        return Response(
            {"message": "Review deleted successfully."},
            status=status.HTTP_200_OK,
        )


class AdminReviewListView(ListAPIView):
    serializer_class = AdminReviewSerializer
    pagination_class = AdminReviewPagination
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Reviews.objects.all()

        search = self.request.query_params.get("search", "").strip()

        if search:
            queryset = queryset.filter(
                Q(text__icontains=search) |
                Q(user__username__icontains=search) |
                Q(car__brand__icontains=search) |
                Q(car__model__icontains=search)
            )

        # Filter by status
        status_param = self.request.query_params.get("status")

        if status_param and status_param != "all":
            queryset = queryset.filter(status=status_param)

        # Filter by rating
        rating = self.request.query_params.get("rating")

        if rating and rating != "all":
            queryset = queryset.filter(rating=rating)

        return queryset.order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        stats = Reviews.objects.aggregate(
            total=Count("id"),
            average_rating=Avg("rating"),
            pending=Count("id", filter=Q(status="pending")),
            approved=Count("id", filter=Q(status="approved")),
        )
        stats["average_rating"] = round(stats["average_rating"] or 0, 1)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data["stats"] = stats
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({"results": serializer.data, "stats": stats})


class AdminReviewStatusView(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def patch(self, request, review_id):
        try:
            review = Reviews.objects.get(id=review_id)
        except Reviews.DoesNotExist:
            return Response(
                {"detail": "Review not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_status = request.data.get("status")

        if new_status not in ["approved", "rejected"]:
            return Response(
                {"detail": "Invalid review status."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_status = review.status
        review.status = new_status
        review.save(update_fields=["status"])

        AdminActivityLog.objects.create(
            admin=request.user,
            action="status_change",
            description=(
                f"Changed review {review.pk} status "
                f"from {old_status} to {new_status}."
            ),
            target_type="review",
            target_id=str(review.pk),
        )

        return Response(
            {
                "message": "Review status updated successfully.",
                "review_id": review.id,
                "status": review.status,
            },
            status=status.HTTP_200_OK,
        )


class AdminDeleteReviewView(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def delete(self, request, review_id):
        try:
            review = Reviews.objects.get(id=review_id)
        except Reviews.DoesNotExist:
            return Response(
                {"detail": "Review not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        delete_review_uploads_from_storage(review.images or [])
        review.delete()

        AdminActivityLog.objects.create(
            admin=request.user,
            action="delete",
            description=f"Deleted review {review_id}.",
            target_type="review",
            target_id=str(review_id),
        )

        return Response(
            {"message": "Review deleted successfully."},
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_helpful(request, review_id):
    review = get_object_or_404(Reviews, pk=review_id)

    with transaction.atomic():

        vote, created = ReviewHelpful.objects.get_or_create(
            review=review,
            user=request.user
        )

        if created:
            Reviews.objects.filter(pk=review.pk).update(
                helpful_count=F("helpful_count") + 1
            )

            helpful = True

        else:
            vote.delete()

            Reviews.objects.filter(pk=review.pk).update(
                helpful_count=F("helpful_count") - 1
            )

            helpful = False

    review.refresh_from_db(fields=["helpful_count"])

    return Response({
        "helpful": helpful,
        "helpful_count": review.helpful_count
    })
