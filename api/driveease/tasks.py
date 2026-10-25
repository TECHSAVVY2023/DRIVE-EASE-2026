from celery import shared_task

from .models import Notification, Booking


@shared_task
def create_notification(
    user_id,
    notification_type,
    title,
    message,
    booking_id=None,
    action_url=None,
):
    booking = None

    if booking_id:
        booking = Booking.objects.get(id=booking_id)
        action_url = f"/client/transaction-details/{booking.booking_reference}"

    Notification.objects.create(
        user_id=user_id,
        notification_type=notification_type,
        title=title,
        message=message,
        action_url=action_url,
        booking=booking,
    )
