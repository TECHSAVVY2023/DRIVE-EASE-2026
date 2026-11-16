from datetime import timedelta

from django.db.models import Q
from django.utils import timezone


PAYMENT_HOLD_MINUTES = 15
BOOKING_BLOCKING_STATUSES = {
    "pending_approval",
    "confirmed",
    "picked_up",
}


def booking_blocks_availability():
    """Return bookings that reserve dates or still have an active payment hold."""
    payment_hold_cutoff = timezone.now() - timedelta(
        minutes=PAYMENT_HOLD_MINUTES,
    )

    return (
        Q(status__in=BOOKING_BLOCKING_STATUSES)
        | Q(
            status="pending_payment",
            created_at__gte=payment_hold_cutoff,
        )
    )
