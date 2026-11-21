"""Bookings API views."""

from datetime import datetime, time, timedelta

from django.db import transaction
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import AdminActivityLog, Booking, Cars, Notification, Payment
from ..pagination import TransactionPagination
from ..serializers import BookingSerializer, TransactionSerializer
from ..utils.notifications import (
    create_admin_notifications,
    create_due_car_availability_notifications,
)
from ..utils.booking_availability import booking_conflicts_with_period
from ..utils.refunds import create_pending_refund


PAID_BOOKING_STATUSES = {
    "pending_approval",
    "confirmed",
    "picked_up",
    "returned",
    "completed",
}

ADMIN_CREATE_BOOKING_STATUSES = {
    "pending_payment",
    "pending_approval",
}

CUSTOMER_CANCELLABLE_STATUSES = {
    "pending_payment",
    "payment_failed",
    "pending_approval",
    "confirmed",
}

# A status can stay unchanged while an admin edits other booking details.
# All other changes must follow the actual rental lifecycle.
BOOKING_STATUS_TRANSITIONS = {
    "pending_payment": {"pending_payment", "pending_approval", "cancelled"},
    "payment_failed": {"payment_failed", "pending_payment", "cancelled"},
    "pending_approval": {"pending_approval", "confirmed", "rejected", "cancelled"},
    "confirmed": {"confirmed", "picked_up", "cancelled"},
    "picked_up": {"picked_up", "returned"},
    "returned": {"returned", "completed"},
    "completed": {"completed"},
    "rejected": {"rejected"},
    "cancelled": {"cancelled"},
}

class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_images = request.user.id_images or {}
        submitted_ids = (
            id_images.get("images")
            if isinstance(id_images, dict)
            else None
        )
        if not isinstance(submitted_ids, list) or not submitted_ids:
            message = (
                "Please upload at least one valid ID image before creating "
                "a booking."
            )
            return Response(
                {
                    "message": message,
                    "id_images": message,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        submitted_car = serializer.validated_data["car"]
        # Serialize availability checks for this car so two simultaneous
        # requests cannot both pass the overlap check.
        car = Cars.objects.select_for_update().get(pk=submitted_car.pk)

        if car.status == "maintenance":
            return Response(
                {"message": "This car is currently under maintenance and cannot be booked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pickup_date = serializer.validated_data["pickup_date"]
        return_date = serializer.validated_data["return_date"]

        overlap = Booking.objects.filter(car=car).filter(
            booking_conflicts_with_period(pickup_date, return_date)
        ).exists()

        if overlap:
            return Response(
                {
                    "message": (
                        "This car is unavailable, temporarily held, or within "
                        "the one-hour turnover buffer. Please choose different times."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking = serializer.save(user=request.user)

        transaction.on_commit(
            lambda: create_admin_notifications(
                notification_type="booking",
                title="New booking created",
                message=(
                    f"Booking {booking.booking_reference} was created and "
                    "is waiting for payment."
                ),
                action_url="/admin/admin-booking",
                booking=booking,
                deduplication_key=f"booking-created:{booking.id}",
            )
        )

        return Response(
            {
                "message": "Booking created successfully.",
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


class ClientCancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, booking_reference):
        booking = get_object_or_404(
            Booking.objects.select_for_update().select_related("car"),
            user=request.user,
            booking_reference=booking_reference,
        )

        reason = str(request.data.get("reason", "")).strip()

        if not reason:
            return Response(
                {"reason": "Please provide a reason for the cancellation."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(reason) > 500:
            return Response(
                {"reason": "Cancellation reason cannot exceed 500 characters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if booking.status not in CUSTOMER_CANCELLABLE_STATUSES:
            return Response(
                {
                    "message": (
                        "This booking can no longer be cancelled online. "
                        "Please contact Drive Ease for assistance."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if booking.status == "confirmed" and booking.pickup_date <= timezone.now():
            return Response(
                {
                    "message": (
                        "A confirmed booking cannot be cancelled online after "
                        "its pickup time. Please contact Drive Ease."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = "cancelled"
        booking.cancel_reason = reason
        booking.save(update_fields=[
            "status",
            "cancel_reason",
            "updated_at",
        ])

        payment = Payment.objects.filter(booking=booking).first()
        refund = None
        refund_created = False
        if payment:
            refund, refund_created = create_pending_refund(
                payment=payment,
                requested_by=request.user,
                customer_reason=reason,
            )

        transaction.on_commit(
            lambda booking_id=booking.id:
                create_admin_notifications(
                    notification_type="booking_status",
                    title="Booking cancelled by customer",
                    message=(
                        f"Booking {booking.booking_reference} was cancelled "
                        f"by the customer. Reason: {reason}"
                    ),
                    action_url="/admin/admin-booking",
                    booking=Booking.objects.get(pk=booking_id),
                    deduplication_key=f"customer-cancelled:{booking_id}",
                )
        )
        if refund_created:
            transaction.on_commit(
                lambda refund_id=refund.id:
                create_admin_notifications(
                    notification_type="payment",
                    title="Refund requires review",
                    message=(
                        f"Booking {booking.booking_reference} was paid through "
                        "PayMongo and has been cancelled. Review its full refund."
                    ),
                    action_url="/admin/admin-booking",
                    booking=booking,
                    deduplication_key=f"refund-review:{refund_id}",
                )
            )
        transaction.on_commit(
            lambda car_id=booking.car_id:
                create_due_car_availability_notifications(
                    car=Cars.objects.get(pk=car_id),
                )
        )

        return Response(
            TransactionSerializer(booking).data,
            status=status.HTTP_200_OK,
        )


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

        # Filter by rental dates. A booking is included when any part of its
        # pickup-to-return interval overlaps the selected calendar period.
        rental_period = self.request.query_params.get("rental_period")
        now = timezone.now()
        today = timezone.localdate()

        def start_of_day(value):
            return timezone.make_aware(
                datetime.combine(value, time.min),
                timezone.get_current_timezone(),
            )

        if rental_period == "today":
            period_start = start_of_day(today)
            period_end = start_of_day(today + timedelta(days=1))
            queryset = queryset.filter(
                pickup_date__lt=period_end,
                return_date__gt=period_start,
            )
        elif rental_period == "next_7_days":
            period_start = start_of_day(today)
            period_end = start_of_day(today + timedelta(days=7))
            queryset = queryset.filter(
                pickup_date__lt=period_end,
                return_date__gt=period_start,
            )
        elif rental_period == "this_month":
            month_start = today.replace(day=1)
            if month_start.month == 12:
                next_month = month_start.replace(
                    year=month_start.year + 1,
                    month=1,
                )
            else:
                next_month = month_start.replace(month=month_start.month + 1)

            queryset = queryset.filter(
                pickup_date__lt=start_of_day(next_month),
                return_date__gt=start_of_day(month_start),
            )
        elif rental_period == "past":
            queryset = queryset.filter(return_date__lte=now)

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

        total = bookings.count()

        stats = {
            "total": total,

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

        # Count bookings grouped by status
        status_counts = {
            item["status"]: item["count"]
            for item in bookings.values("status").annotate(
                count=Count("id")
            )
        }

        # Include every available status, even if its count is zero
        distribution = []

        for status_value, status_label in Booking.BOOKING_STATUS:
            count = status_counts.get(status_value, 0)

            percentage = (
                round((count / total) * 100, 1)
                if total > 0 else 0
            )

            distribution.append({
                "status": status_value,
                "label": status_label,
                "count": count,
                "percentage": percentage,
            })

        stats["status_distribution"] = distribution

        return Response(stats)

class AdminCreateBookingView(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request):
        initial_status = request.data.get("status", "pending_payment")

        if initial_status not in ADMIN_CREATE_BOOKING_STATUSES:
            return Response(
                {
                    "status": (
                        "A new booking must start as Pending Payment or "
                        "Pending Approval. Use Edit Booking for later stages."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submitted_car = serializer.validated_data["car"]
        car = Cars.objects.select_for_update().get(pk=submitted_car.pk)

        if car.status == "maintenance":
            return Response(
                {"message": "This car is currently under maintenance and cannot be booked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pickup_date = serializer.validated_data["pickup_date"]
        return_date = serializer.validated_data["return_date"]

        if Booking.objects.filter(car=car).filter(
            booking_conflicts_with_period(pickup_date, return_date)
        ).exists():
            return Response(
                {
                    "message": (
                        "This car is unavailable, temporarily held, or within "
                        "the one-hour turnover buffer. Please choose different times."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking = serializer.save()

        is_paid = booking.status in PAID_BOOKING_STATUSES

        Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            currency="PHP",
            status="paid" if is_paid else "pending",
            payment_method=(
                request.data.get("payment_method", "manual")
                if is_paid
                else None
            ),
            paid_at=timezone.now() if is_paid else None,
        )

        AdminActivityLog.objects.create(
            admin=request.user,
            action="create",
            description=f"Created booking {booking.booking_reference}.",
            target_type="booking",
            target_id=booking.booking_reference,
        )

        return Response(
            {
                "message": "Booking created successfully.",
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

        requested_status = request.data.get("status", old_status)
        allowed_statuses = BOOKING_STATUS_TRANSITIONS.get(
            old_status,
            {old_status},
        )

        if requested_status not in allowed_statuses:
            return Response(
                {
                    "status": (
                        f"A booking cannot move directly from {old_status} "
                        f"to {requested_status}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = BookingSerializer(
            booking,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        submitted_car = serializer.validated_data.get("car", booking.car)
        car = Cars.objects.select_for_update().get(pk=submitted_car.pk)

        if car.status == "maintenance":
            return Response(
                {"message": "This car is currently under maintenance and cannot be booked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pickup_date = serializer.validated_data.get(
            "pickup_date",
            booking.pickup_date,
        )
        return_date = serializer.validated_data.get(
            "return_date",
            booking.return_date,
        )

        if Booking.objects.filter(car=car).exclude(pk=booking.pk).filter(
            booking_conflicts_with_period(pickup_date, return_date)
        ).exists():
            return Response(
                {
                    "message": (
                        "This car is unavailable, temporarily held, or within "
                        "the one-hour turnover buffer. Please choose different times."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking = serializer.save()

        if booking.status in PAID_BOOKING_STATUSES:
            payment, _ = Payment.objects.get_or_create(
                booking=booking,
                defaults={
                    "amount": booking.total_price,
                    "currency": "PHP",
                    "status": "pending",
                },
            )

            payment.amount = booking.total_price
            payment.status = "paid"
            payment.payment_method = (
                request.data.get("payment_method")
                or payment.payment_method
                or "manual"
            )

            if payment.paid_at is None:
                payment.paid_at = timezone.now()

            payment.save(update_fields=[
                "amount",
                "status",
                "payment_method",
                "paid_at",
                "updated_at",
            ])

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
                # Keep the notification in the same database transaction as
                # the status change so both changes succeed or fail together.
                Notification.objects.get_or_create(
                    user_id=booking.user_id,
                    deduplication_key=(
                        f"booking-status:{booking.id}:{booking.status}"
                    ),
                    defaults={
                        "notification_type": "booking_status",
                        "title": notification[0],
                        "message": notification[1],
                        "action_url": (
                            "/client/transaction-details/"
                            f"{booking.booking_reference}"
                        ),
                        "booking": booking,
                    },
                )

            if booking.status in {"returned", "completed", "cancelled", "rejected"}:
                create_due_car_availability_notifications(
                    car=booking.car,
                )

        AdminActivityLog.objects.create(
            admin=request.user,
            action="update",
            description=f"Updated booking {booking.booking_reference}.",
            target_type="booking",
            target_id=booking.booking_reference,
        )

        return Response(
            {
                "message": "Booking updated successfully.",
                "booking_reference": booking.booking_reference,
            },
            status=status.HTTP_200_OK,
        )


class AdminBookingDeleteView(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def delete(self, request, booking_reference):
        booking = get_object_or_404(Booking, booking_reference=booking_reference)

        car_id = booking.car_id
        booking_label = booking.booking_reference

        booking.delete()

        AdminActivityLog.objects.create(
            admin=request.user,
            action="delete",
            description=f"Deleted booking {booking_label}.",
            target_type="booking",
            target_id=booking_label,
        )

        transaction.on_commit(
            lambda: create_due_car_availability_notifications(
                car=Cars.objects.get(pk=car_id),
            )
        )

        return Response(
            {"message": "Booking deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
