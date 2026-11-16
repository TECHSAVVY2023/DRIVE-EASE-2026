"""Admin analytics API views."""

import math
from datetime import timedelta

from django.db.models import Avg, Count, Sum
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Booking, Cars, Payment


ALLOWED_PERIODS = {30, 90, 180, 365}
PERIOD_LABELS = {
    30: "Last 30 days",
    90: "Last 3 months",
    180: "Last 6 months",
    365: "Last 12 months",
}
REVENUE_POINT_COUNTS = {30: 5, 90: 6, 180: 6, 365: 12}
UTILIZED_BOOKING_STATUSES = {
    "confirmed",
    "picked_up",
    "returned",
    "completed",
}


def parse_period(request):
    try:
        period = int(request.query_params.get("period", 30))
    except (TypeError, ValueError):
        return None

    return period if period in ALLOWED_PERIODS else None


def period_bounds(period):
    end = timezone.localdate() + timedelta(days=1)
    start = end - timedelta(days=period)
    previous_start = start - timedelta(days=period)
    return start, end, previous_start, start


def percentage_change(current, previous):
    if previous == 0:
        return None
    return round(float((current - previous) / previous * 100), 1)


def paid_revenue(start, end):
    return Payment.objects.filter(
        status="paid",
        paid_at__date__gte=start,
        paid_at__date__lt=end,
    ).aggregate(total=Sum("amount"))["total"] or 0


def fleet_utilization(start, end):
    fleet_size = Cars.objects.count()
    period_days = (end - start).days
    if not fleet_size or not period_days:
        return 0

    bookings = Booking.objects.filter(
        status__in=UTILIZED_BOOKING_STATUSES,
        pickup_date__date__lt=end,
        return_date__date__gte=start,
    ).only("pickup_date", "return_date")

    utilized_days = 0
    for booking in bookings:
        pickup_date = timezone.localtime(booking.pickup_date).date()
        return_date = timezone.localtime(booking.return_date).date()
        overlap_start = max(pickup_date, start)
        overlap_end = min(return_date, end)
        utilized_days += max((overlap_end - overlap_start).days, 0)

    capacity_days = fleet_size * period_days
    return round(min(utilized_days / capacity_days * 100, 100), 1)


class AdminAnalyticsStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        period = parse_period(request)
        if period is None:
            return Response(
                {"detail": "Period must be one of: 30, 90, 180, 365."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start, end, previous_start, previous_end = period_bounds(period)

        current_bookings = Booking.objects.filter(
            created_at__date__gte=start,
            created_at__date__lt=end,
        )
        previous_bookings = Booking.objects.filter(
            created_at__date__gte=previous_start,
            created_at__date__lt=previous_end,
        )

        current_booking_count = current_bookings.count()
        previous_booking_count = previous_bookings.count()
        current_revenue = paid_revenue(start, end)
        previous_revenue = paid_revenue(previous_start, previous_end)
        current_utilization = fleet_utilization(start, end)
        previous_utilization = fleet_utilization(previous_start, previous_end)

        current_cancellations = current_bookings.filter(status="cancelled").count()
        previous_cancellations = previous_bookings.filter(status="cancelled").count()
        current_cancellation_rate = round(
            current_cancellations / current_booking_count * 100,
            1,
        ) if current_booking_count else 0
        previous_cancellation_rate = round(
            previous_cancellations / previous_booking_count * 100,
            1,
        ) if previous_booking_count else 0

        return Response({
            "period": period,
            "label": PERIOD_LABELS[period],
            "total_revenue": float(current_revenue),
            "revenue_change": percentage_change(current_revenue, previous_revenue),
            "total_bookings": current_booking_count,
            "bookings_change": percentage_change(
                current_booking_count,
                previous_booking_count,
            ),
            "fleet_utilization": current_utilization,
            "fleet_utilization_change": percentage_change(
                current_utilization,
                previous_utilization,
            ),
            "cancellation_rate": current_cancellation_rate,
            "cancellation_rate_change": percentage_change(
                current_cancellation_rate,
                previous_cancellation_rate,
            ),
        })


class AdminAnalyticsRevenueView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        period = parse_period(request)
        if period is None:
            return Response(
                {"detail": "Period must be one of: 30, 90, 180, 365."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start, end, previous_start, previous_end = period_bounds(period)
        total = paid_revenue(start, end)
        previous_total = paid_revenue(previous_start, previous_end)
        point_count = REVENUE_POINT_COUNTS[period]
        bucket_days = math.ceil(period / point_count)
        points = []
        bucket_start = start

        while bucket_start < end:
            bucket_end = min(bucket_start + timedelta(days=bucket_days), end)
            bucket_total = paid_revenue(bucket_start, bucket_end)

            if period == 365:
                point_label = bucket_start.strftime("%b")
            elif bucket_start.month == (bucket_end - timedelta(days=1)).month:
                point_label = (
                    f"{bucket_start.strftime('%b')} {bucket_start.day}-"
                    f"{(bucket_end - timedelta(days=1)).day}"
                )
            else:
                point_label = bucket_start.strftime("%b %d")

            points.append({
                "label": point_label,
                "value": float(bucket_total),
            })
            bucket_start = bucket_end

        return Response({
            "period": period,
            "label": PERIOD_LABELS[period],
            "total": float(total),
            "previous_total": float(previous_total),
            "percentage_change": percentage_change(total, previous_total),
            "points": points,
        })


class AdminAnalyticsStatusDistributionView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        period = parse_period(request)
        if period is None:
            return Response(
                {"detail": "Period must be one of: 30, 90, 180, 365."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start, end, _, _ = period_bounds(period)
        bookings = Booking.objects.filter(
            created_at__date__gte=start,
            created_at__date__lt=end,
        )
        total = bookings.count()
        status_counts = {
            item["status"]: item["count"]
            for item in bookings.values("status").annotate(count=Count("id"))
        }
        distribution = []

        for status_value, status_label in Booking.BOOKING_STATUS:
            status_count = status_counts.get(status_value, 0)
            distribution.append({
                "status": status_value,
                "label": status_label,
                "count": status_count,
                "percentage": round(
                    status_count / total * 100,
                    1,
                ) if total else 0,
            })

        return Response({
            "period": period,
            "label": PERIOD_LABELS[period],
            "total": total,
            "status_distribution": distribution,
        })


class AdminAnalyticsTopVehiclesView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        period = parse_period(request)
        if period is None:
            return Response(
                {"detail": "Period must be one of: 30, 90, 180, 365."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start, end, _, _ = period_bounds(period)
        vehicles = list(
            Booking.objects.filter(
                status="completed",
                completed_at__date__gte=start,
                completed_at__date__lt=end,
            )
            .values(
                "car__car_reference",
                "car__brand",
                "car__model",
            )
            .annotate(bookings=Count("id"))
            .order_by("-bookings", "car__brand", "car__model")[:4]
        )
        highest_booking_count = vehicles[0]["bookings"] if vehicles else 0

        return Response({
            "period": period,
            "label": PERIOD_LABELS[period],
            "vehicles": [
                {
                    "car_reference": vehicle["car__car_reference"],
                    "name": f'{vehicle["car__brand"]} {vehicle["car__model"]}',
                    "bookings": vehicle["bookings"],
                    "score": round(
                        vehicle["bookings"] / highest_booking_count * 100,
                        1,
                    ) if highest_booking_count else 0,
                }
                for vehicle in vehicles
            ],
        })


class AdminAnalyticsCustomerInsightsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        period = parse_period(request)
        if period is None:
            return Response(
                {"detail": "Period must be one of: 30, 90, 180, 365."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start, end, _, _ = period_bounds(period)
        completed_bookings = Booking.objects.filter(
            status="completed",
            completed_at__date__gte=start,
            completed_at__date__lt=end,
        )
        customer_ids = completed_bookings.values_list(
            "user_id",
            flat=True,
        ).distinct()
        customer_count = customer_ids.count()
        returning_customers = (
            Booking.objects.filter(
                user_id__in=customer_ids,
                status="completed",
                completed_at__date__lt=start,
            )
            .values("user_id")
            .distinct()
            .count()
        )
        new_customers = customer_count - returning_customers
        averages = completed_bookings.aggregate(
            rental_days=Avg("number_of_days"),
            booking_value=Avg("total_price"),
        )

        return Response({
            "period": period,
            "label": PERIOD_LABELS[period],
            "new_customers": new_customers,
            "new_customer_percentage": round(
                new_customers / customer_count * 100,
                1,
            ) if customer_count else 0,
            "returning_customers": returning_customers,
            "return_rate": round(
                returning_customers / customer_count * 100,
                1,
            ) if customer_count else 0,
            "average_rental_days": round(
                float(averages["rental_days"] or 0),
                1,
            ),
            "average_booking_value": round(
                float(averages["booking_value"] or 0),
                2,
            ),
        })
