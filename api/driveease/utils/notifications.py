from django.contrib.auth import get_user_model
from django.utils import timezone

from ..models import Booking, CarAvailabilityAlert, Cars, Notification


User = get_user_model()


def create_notification(
    *,
    user_id,
    notification_type,
    title,
    message,
    booking_id=None,
    action_url=None,
):
    """Create one in-app notification directly in the database."""
    booking = None

    if booking_id is not None:
        booking = Booking.objects.get(pk=booking_id)
        action_url = (
            f"/client/transaction-details/{booking.booking_reference}"
        )

    return Notification.objects.create(
        user_id=user_id,
        notification_type=notification_type,
        title=title,
        message=message,
        action_url=action_url,
        booking=booking,
    )


def car_is_currently_rented(car):
    """Match the current-rental rule used by the client car details page."""
    now = timezone.now()
    return car.bookings.filter(
        status__in=["pending_approval", "confirmed", "picked_up"],
        pickup_date__lte=now,
        return_date__gt=now,
    ).exists()


def create_due_car_availability_notifications(*, user=None, car=None):
    """Resolve one-time alerts whose cars are now available.

    This is intentionally safe to call from both booking updates and the user
    notification endpoints. The latter lets alerts work without a cron worker.
    """
    alerts = CarAvailabilityAlert.objects.select_related("car", "user")

    if user is not None:
        alerts = alerts.filter(user=user)
    if car is not None:
        alerts = alerts.filter(car=car)

    notified = 0
    for alert in alerts:
        if alert.car.status != "available":
            continue
        if car_is_currently_rented(alert.car):
            continue

        Notification.objects.get_or_create(
            user=alert.user,
            deduplication_key=f"car-available:{alert.id}",
            defaults={
                "notification_type": "reminder",
                "title": "Car Now Available",
                "message": (
                    f"{alert.car.brand} {alert.car.model} is now available "
                    "to book."
                ),
                "action_url": (
                    f"/client/car-details/{alert.car.car_reference}"
                ),
            },
        )
        alert.delete()
        notified += 1

    return notified


def create_admin_notifications(
    *,
    notification_type,
    title,
    message,
    action_url=None,
    booking=None,
    deduplication_key=None,
):
    """Create a personal notification for every active staff account."""
    admin_ids = User.objects.filter(
        is_active=True,
        is_staff=True,
    ).values_list("id", flat=True)

    notifications = [
        Notification(
            user_id=admin_id,
            notification_type=notification_type,
            title=title,
            message=message,
            action_url=action_url,
            booking=booking,
            deduplication_key=deduplication_key,
        )
        for admin_id in admin_ids
    ]

    if notifications:
        Notification.objects.bulk_create(
            notifications,
            ignore_conflicts=bool(deduplication_key),
        )

    return len(notifications)


def create_due_admin_notifications():
    """Create daily maintenance and overdue alerts without a cron worker."""
    today = timezone.localdate().isoformat()
    now = timezone.now()

    maintenance_cars = Cars.objects.filter(status="maintenance").only(
        "id",
        "car_reference",
        "brand",
        "model",
    )
    for car in maintenance_cars:
        create_admin_notifications(
            notification_type="reminder",
            title="Vehicle requires maintenance",
            message=(
                f"{car.brand} {car.model} ({car.car_reference}) is currently "
                "marked for maintenance."
            ),
            action_url="/admin/admin-fleet",
            deduplication_key=f"maintenance:{car.id}:{today}",
        )

    overdue_bookings = Booking.objects.filter(
        status__in=["confirmed", "picked_up"],
        return_date__lt=now,
    ).select_related("car")
    for booking in overdue_bookings:
        create_admin_notifications(
            notification_type="reminder",
            title="Rental is overdue",
            message=(
                f"Booking {booking.booking_reference} for "
                f"{booking.car.brand} {booking.car.model} is past its return date."
            ),
            action_url="/admin/admin-booking",
            booking=booking,
            deduplication_key=f"booking-overdue:{booking.id}:{today}",
        )
