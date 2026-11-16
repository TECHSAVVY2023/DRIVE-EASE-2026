from django.core.management.base import BaseCommand

from driveease.models import Booking, Cars, Payment, Reviews
from driveease.utils.notifications import create_admin_notifications


class Command(BaseCommand):
    help = "Create admin notifications for existing DriveEase records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show how many records would be processed without writing.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        processed = 0

        records = []

        for booking in Booking.objects.select_related("car"):
            records.append({
                "notification_type": "booking",
                "title": "Existing booking",
                "message": (
                    f"Booking {booking.booking_reference} currently has "
                    f"status {booking.get_status_display()}."
                ),
                "action_url": "/admin/admin-booking",
                "booking": booking,
                "deduplication_key": f"historical-booking:{booking.id}",
            })

        for payment in Payment.objects.select_related("booking"):
            records.append({
                "notification_type": "payment",
                "title": "Existing payment",
                "message": (
                    f"Payment for booking "
                    f"{payment.booking.booking_reference} currently has "
                    f"status {payment.get_status_display()}."
                ),
                "action_url": "/admin/admin-booking",
                "booking": payment.booking,
                "deduplication_key": f"historical-payment:{payment.id}",
            })

        for review in Reviews.objects.select_related("car"):
            records.append({
                "notification_type": "review",
                "title": "Existing review",
                "message": (
                    f"A {review.rating}-star review for "
                    f"{review.car.brand} {review.car.model} currently has "
                    f"status {review.get_status_display()}."
                ),
                "action_url": "/admin/admin-review",
                "deduplication_key": f"historical-review:{review.id}",
            })

        for car in Cars.objects.filter(status="maintenance"):
            records.append({
                "notification_type": "reminder",
                "title": "Vehicle requires maintenance",
                "message": (
                    f"{car.brand} {car.model} ({car.car_reference}) is "
                    "currently marked for maintenance."
                ),
                "action_url": "/admin/admin-fleet",
                "deduplication_key": f"historical-maintenance:{car.id}",
            })

        if not dry_run:
            for payload in records:
                create_admin_notifications(**payload)
                processed += 1
        else:
            processed = len(records)

        verb = "would process" if dry_run else "processed"
        self.stdout.write(
            self.style.SUCCESS(
                f"Admin notification backfill {verb} {processed} records."
            )
        )
