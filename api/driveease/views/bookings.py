"""Bookings API views."""

from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import AdminActivityLog, Booking
from ..pagination import TransactionPagination
from ..serializers import BookingSerializer, TransactionSerializer
from ..tasks import create_notification

class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        car = serializer.validated_data["car"]
        pickup_date = serializer.validated_data["pickup_date"]
        return_date = serializer.validated_data["return_date"]

        overlap = Booking.objects.filter(
            car=car,
            status__in=[
                "pending_approval",
                "confirmed",
                "picked_up",
            ],
            pickup_date__lt=return_date,
            return_date__gt=pickup_date,
        ).exists()

        if overlap:
            return Response(
                {
                    "message": "This car is unavailable during the selected period."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate booking reference if not provided
        if not serializer.validated_data.get("booking_reference"):
            import uuid
            serializer.validated_data["booking_reference"] = (
                f"BKG-{uuid.uuid4().hex[:10].upper()}"
            )

        booking = serializer.save()

        create_notification.delay(
            user_id=request.user.id,
            notification_type="booking",
            title="Booking Created",
            message=(
                f"Your booking {booking.booking_reference} "
                "has been submitted successfully."
            ),
            booking_id=booking.id,
        )

        return Response(
            {
                "message": "Booking created successfully.",
                "booking_id": booking.id,
                "booking_reference": booking.booking_reference,
            },
            status=status.HTTP_201_CREATED,
        )


class TransactionListView(ListAPIView):
    serializer_class = TransactionSerializer
    pagination_class = TransactionPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            Booking.objects
            .filter(user=self.request.user)
            .select_related("car")
        )

        # Search
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(booking_reference__icontains=search) |
                Q(car__brand__icontains=search) |
                Q(car__model__icontains=search)
            )

        # Filter by status
        status_param = self.request.query_params.get("status")

        if status_param and status_param != "all":
            statuses = [
                item.strip()
                for item in status_param.split(",")
                if item.strip()
            ]

            if statuses:
                queryset = queryset.filter(
                    status__in=statuses
                )

        # Sort
        sort = self.request.query_params.get("sort")

        if sort == "oldest":
            queryset = queryset.order_by("created_at")

        elif sort == "highest":
            queryset = queryset.order_by("-total_price")

        elif sort == "lowest":
            queryset = queryset.order_by("total_price")

        else:
            queryset = queryset.order_by("-created_at")

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "results": serializer.data,
        })


class TransactionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_reference):
        try:
            booking = (
                Booking.objects
                .filter(
                    user=request.user,
                    booking_reference=booking_reference,
                )
                .select_related("car")
                .get()
            )

        except Booking.DoesNotExist:
            return Response(
                {"detail": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TransactionSerializer(booking)

        return Response(serializer.data)


class AdminBookingListView(ListAPIView):
    serializer_class = TransactionSerializer
    pagination_class = TransactionPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            Booking.objects
            .select_related("user", "car", "payments")
        )

        # Search
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(booking_reference__icontains=search) |
                Q(car__brand__icontains=search) |
                Q(car__model__icontains=search) |
                Q(user__given_name__icontains=search) |
                Q(user__family_name__icontains=search) |
                Q(user__email__icontains=search)
            )
            
        # Filter by status
        status_param = self.request.query_params.get("status")

        if status_param and status_param != "all":
            statuses = [
                item.strip()
                for item in status_param.split(",")
                if item.strip()
            ]

            if "overdue" in statuses:
                queryset = queryset.filter(
                    status__in=["confirmed", "picked_up"],
                    return_date__lt=timezone.now(),
                )

            elif statuses:
                queryset = queryset.filter(
                    status__in=statuses
                )

        # Filter by payment status
        payment_status = self.request.query_params.get("payment_status")

        if payment_status and payment_status != "all":
            payment_statuses = [
                item.strip()
                for item in payment_status.split(",")
                if item.strip()
            ]

            if payment_statuses:
                queryset = queryset.filter(
                    payments__status__in=payment_statuses
                )

        # Sort
        sort = self.request.query_params.get("sort")

        if sort == "oldest":
            queryset = queryset.order_by("created_at")

        elif sort == "highest":
            queryset = queryset.order_by("-total_price")

        elif sort == "lowest":
            queryset = queryset.order_by("total_price")

        else:
            queryset = queryset.order_by("-created_at")

        return queryset


class AdminBookingStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        bookings = Booking.objects.all()

        stats = {
            "total": bookings.count(),

            "pending_approval": bookings.filter(
                status="pending_approval"
            ).count(),

            "active_rentals": bookings.filter(
                status__in=[
                    "confirmed",
                    "picked_up",
                    "returned",
                ]
            ).count(),

            "completed": bookings.filter(
                status="completed"
            ).count(),

            "cancelled": bookings.filter(
                status="cancelled"
            ).count(),
        }

        return Response(stats)


class AdminCreateBookingView(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not serializer.validated_data.get("booking_reference"):
            import uuid
            serializer.validated_data["booking_reference"] = (
                f"BKG-{uuid.uuid4().hex[:10].upper()}"
            )

        booking = serializer.save()

        AdminActivityLog.objects.create(
            admin=request.user,
            action="create",
            description=f"Created booking {booking.booking_reference}.",
            target_type="booking",
            target_id=str(booking.pk),
        )

        return Response(
            {
                "message": "Booking created successfully.",
                "booking_id": booking.id,
                "booking_reference": booking.booking_reference,
            },
            status=status.HTTP_201_CREATED,
        )


class AdminUpdateBookingView(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def patch(self, request, booking_reference):
        try:
            booking = Booking.objects.get(
                booking_reference=booking_reference
            )
        except Booking.DoesNotExist:
            return Response(
                {"message": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        old_status = booking.status

        serializer = BookingSerializer(
            booking,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        booking = serializer.save()

        # Notify the user when the booking status changes
        if old_status != booking.status:
            notifications = {
                "confirmed": (
                    "Booking Confirmed",
                    f"Your booking {booking.booking_reference} has been confirmed.",
                ),
                "rejected": (
                    "Booking Rejected",
                    f"Your booking {booking.booking_reference} has been rejected.",
                ),
                "picked_up": (
                    "Vehicle Picked Up",
                    f"Your booking {booking.booking_reference} has been marked as picked up.",
                ),
                "returned": (
                    "Vehicle Returned",
                    f"Your booking {booking.booking_reference} has been marked as returned.",
                ),
                "completed": (
                    "Booking Completed",
                    f"Your booking {booking.booking_reference} has been completed.",
                ),
                "cancelled": (
                    "Booking Cancelled",
                    f"Your booking {booking.booking_reference} has been cancelled.",
                ),
            }

            notification = notifications.get(booking.status)

            if notification:
                transaction.on_commit(
                    lambda uid=booking.user_id,
                           title=notification[0],
                           message=notification[1],
                           booking_id=booking.id:
                        create_notification.delay(
                            user_id=uid,
                            notification_type="booking_status",
                            title=title,
                            message=message,
                            booking_id=booking_id,
                        )
                )

        AdminActivityLog.objects.create(
            admin=request.user,
            action="update",
            description=f"Updated booking {booking.booking_reference}.",
            target_type="booking",
            target_id=str(booking.pk),
        )

        return Response(
            {
                "message": "Booking updated successfully.",
                "booking_id": booking.id,
                "booking_reference": booking.booking_reference,
            },
            status=status.HTTP_200_OK,
        )


class AdminBookingDeleteView(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def delete(self, request, booking_reference):
        booking = get_object_or_404(Booking, booking_reference=booking_reference)

        booking_id = booking.pk
        booking_label = booking.booking_reference

        booking.delete()

        AdminActivityLog.objects.create(
            admin=request.user,
            action="delete",
            description=f"Deleted booking {booking_label}.",
            target_type="booking",
            target_id=str(booking_id),
        )

        return Response(
            {"message": "Booking deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
