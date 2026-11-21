from datetime import timedelta

from django.db.models import Q
from django.utils import timezone


PAYMENT_HOLD_MINUTES = 15
BOOKING_TURNAROUND_BUFFER_MINUTES = 60
BOOKING_TURNAROUND_BUFFER = timedelta(
    minutes=BOOKING_TURNAROUND_BUFFER_MINUTES,
)
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
    turnover_buffer_cutoff = timezone.now() - BOOKING_TURNAROUND_BUFFER

    return (
        Q(status__in=BOOKING_BLOCKING_STATUSES)
        | Q(
            status__in={"returned", "completed"},
            returned_at__gte=turnover_buffer_cutoff,
        )
        | Q(
            status__in={"returned", "completed"},
            returned_at__isnull=True,
            return_date__gte=turnover_buffer_cutoff,
        )
        | Q(
            status="pending_payment",
            created_at__gte=payment_hold_cutoff,
        )
    )


def car_is_available_for_booking(car, at=None):
    """Return whether a car is free at a moment under the booking rules."""
    at = at or timezone.now()

    if car.status != "available":
        return False

    return not car.bookings.filter(
        booking_conflicts_with_period(at, at),
    ).exists()


def booking_conflicts_with_period(pickup_date, return_date):
    """Block overlapping reservations, turnover time, and overdue rentals.

    Once an active booking is overdue, its real return time is unknown. It
    therefore blocks every future period until an admin moves it to a
    non-blocking status such as returned, completed, cancelled, or rejected.
    """
    now = timezone.now()
    overlaps_selected_period = Q(
        pickup_date__lt=return_date + BOOKING_TURNAROUND_BUFFER,
        return_date__gt=pickup_date - BOOKING_TURNAROUND_BUFFER,
    )
    unresolved_overdue_rental = Q(
        status__in=BOOKING_BLOCKING_STATUSES,
        pickup_date__lte=now,
        return_date__lte=now,
    )

    return booking_blocks_availability() & (
        overlaps_selected_period | unresolved_overdue_rental
    )
