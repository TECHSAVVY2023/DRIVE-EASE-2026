"""User and admin notification API views."""

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import CarAvailabilityAlert, Cars, Notification
from ..pagination import NotificationPagination
from ..serializers import NotificationSerializer
from ..utils.booking_availability import car_is_available_for_booking
from ..utils.notifications import (
    create_due_admin_notifications,
    create_due_car_availability_notifications,
)


class UserNotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationPagination

    def get_queryset(self):
        create_due_car_availability_notifications(user=self.request.user)
        return (
            Notification.objects
            .filter(user=self.request.user)
            .select_related("booking")
            .order_by("-created_at")
        )


class UserUnreadNotificationCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        create_due_car_availability_notifications(user=request.user)
        return Response({
            "unread_count": Notification.objects.filter(
                user=request.user,
                is_read=False,
            ).count()
        })


class MarkNotificationAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            user=request.user,
        )
        mark_notification_read(notification)
        return Response({"message": "Notification marked as read."})


class UserMarkAllNotificationsAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        updated = Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).update(is_read=True, read_at=timezone.now())

        return Response({
            "message": "All notifications marked as read.",
            "updated": updated,
        })


class UserDeleteAllNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        deleted, _ = Notification.objects.filter(
            user=request.user,
        ).delete()

        return Response({
            "message": "All notifications deleted.",
            "deleted": deleted,
        })


class CarAvailabilityAlertView(APIView):
    permission_classes = [IsAuthenticated]

    def get_car(self, car_reference):
        return get_object_or_404(Cars, car_reference=car_reference)

    def get(self, request, car_reference):
        car = self.get_car(car_reference)
        return Response({
            "subscribed": CarAvailabilityAlert.objects.filter(
                user=request.user,
                car=car,
            ).exists(),
        })

    def post(self, request, car_reference):
        car = self.get_car(car_reference)

        if car_is_available_for_booking(car):
            return Response(
                {"message": "This car is already available to book."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        _, created = CarAvailabilityAlert.objects.get_or_create(
            user=request.user,
            car=car,
        )
        return Response(
            {
                "subscribed": True,
                "message": (
                    "You will be notified when this car becomes available."
                    if created else
                    "You are already subscribed to this availability alert."
                ),
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def delete(self, request, car_reference):
        car = self.get_car(car_reference)
        CarAvailabilityAlert.objects.filter(
            user=request.user,
            car=car,
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminNotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]
    pagination_class = NotificationPagination

    def get_queryset(self):
        create_due_admin_notifications()

        queryset = (
            Notification.objects
            .filter(user=self.request.user)
            .select_related("booking")
        )

        search = self.request.query_params.get("search", "").strip()
        notification_type = self.request.query_params.get("type", "").strip()
        unread = self.request.query_params.get("unread", "").lower()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(message__icontains=search)
            )
        if notification_type and notification_type != "all":
            queryset = queryset.filter(notification_type=notification_type)
        if unread in {"1", "true"}:
            queryset = queryset.filter(is_read=False)

        return queryset.order_by("-created_at")


class AdminUnreadNotificationCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        create_due_admin_notifications()

        return Response({
            "unread_count": Notification.objects.filter(
                user=request.user,
                is_read=False,
            ).count()
        })


class AdminMarkNotificationAsReadView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            user=request.user,
        )
        mark_notification_read(notification)
        return Response({"message": "Notification marked as read."})


class AdminMarkAllNotificationsAsReadView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request):
        updated = Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).update(is_read=True, read_at=timezone.now())

        return Response({
            "message": "All notifications marked as read.",
            "updated": updated,
        })


class AdminDeleteNotificationView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            user=request.user,
        )
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def mark_notification_read(notification):
    if notification.is_read:
        return

    notification.is_read = True
    notification.read_at = timezone.now()
    notification.save(update_fields=["is_read", "read_at"])
