"""Dashboard API views."""

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..pagination import ( 
    ReviewPagination, FleetPagination, TransactionPagination, 
    NotificationPagination, AccountsPagination, AdminReviewPagination
)
from rest_framework.decorators import api_view, permission_classes
from ..models import ContactListModel, Cars, Reviews, ReviewHelpful, FileUploadModel, Booking, Payment, Notification, Accounts, CarType, Feature
from ..serializers import ContactListSerializer
from ..forms import ContactListForm
from ..filter_options import get_filter_options
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..tasks import create_notification
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F
from django.db.models import Exists, OuterRef
from django.db.models.fields import capfirst
from django.db.models import Avg, Count, Q, Sum
from django.db.models import Case, When, Value, BooleanField
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
import traceback
import requests
import json
import calendar
from datetime import datetime, timedelta
from ..serializers import (
    ReviewSerializer, CarSerializer, FileUploadSerializer, BookingSerializer,
    PaymentSerializer, TransactionSerializer, NotificationSerializer, AccountsSerializer,
    CarCreateSerializer, CarTypeSerializer, FeatureSerializer, CarUpdateSerializer,
    AdminReviewSerializer,
)

class AdminDashboardRevenueView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        month_param = request.query_params.get("month")
        today = timezone.localdate()

        try:
            selected_month = (
                datetime.strptime(month_param, "%Y-%m").date().replace(day=1)
                if month_param
                else today.replace(day=1)
            )
        except ValueError:
            return Response(
                {"detail": "Month must use the YYYY-MM format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if selected_month.month == 12:
            next_month = selected_month.replace(
                year=selected_month.year + 1,
                month=1,
            )
        else:
            next_month = selected_month.replace(month=selected_month.month + 1)

        previous_month_last_day = selected_month - timedelta(days=1)
        previous_month = previous_month_last_day.replace(day=1)

        paid_payments = Payment.objects.filter(
            status="paid",
            paid_at__date__gte=selected_month,
            paid_at__date__lt=next_month,
        )

        total = paid_payments.aggregate(total=Sum("amount"))["total"] or 0
        previous_total = Payment.objects.filter(
            status="paid",
            paid_at__date__gte=previous_month,
            paid_at__date__lt=selected_month,
        ).aggregate(total=Sum("amount"))["total"] or 0

        if previous_total:
            percentage_change = ((total - previous_total) / previous_total) * 100
        elif total:
            percentage_change = 100
        else:
            percentage_change = 0

        days_in_month = calendar.monthrange(
            selected_month.year,
            selected_month.month,
        )[1]
        points = []

        for start_day in range(1, days_in_month + 1, 7):
            end_day = min(start_day + 6, days_in_month)
            week_total = paid_payments.filter(
                paid_at__day__gte=start_day,
                paid_at__day__lte=end_day,
            ).aggregate(total=Sum("amount"))["total"] or 0

            points.append({
                "label": f"{start_day}-{end_day}",
                "value": float(week_total),
            })

        return Response({
            "month": selected_month.strftime("%Y-%m"),
            "label": selected_month.strftime("%B %Y"),
            "total": float(total),
            "previous_total": float(previous_total),
            "percentage_change": round(float(percentage_change), 1),
            "points": points,
        })

class AdminDashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def calculate_change(current, previous):
        if previous == 0:
            return None

        return round(float((current - previous) / previous * 100), 1)

    def get(self, request):
        month_param = request.query_params.get("month")
        today = timezone.localdate()

        try:
            current_month = (
                datetime.strptime(month_param, "%Y-%m").date().replace(day=1)
                if month_param
                else today.replace(day=1)
            )
        except ValueError:
            return Response(
                {"detail": "Month must use the YYYY-MM format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        previous_month_end = current_month - timedelta(days=1)
        previous_month = previous_month_end.replace(day=1)

        if current_month.month == 12:
            next_month = current_month.replace(
                year=current_month.year + 1,
                month=1,
            )
        else:
            next_month = current_month.replace(
                month=current_month.month + 1
            )

        bookings = Booking.objects.all()

        current_bookings = bookings.filter(
            created_at__date__gte=current_month,
            created_at__date__lt=next_month,
        ).count()

        previous_bookings = bookings.filter(
            created_at__date__gte=previous_month,
            created_at__date__lt=current_month,
        ).count()

        current_revenue = Payment.objects.filter(
            status="paid",
            paid_at__date__gte=current_month,
            paid_at__date__lt=next_month,
        ).aggregate(total=Sum("amount"))["total"] or 0

        previous_revenue = Payment.objects.filter(
            status="paid",
            paid_at__date__gte=previous_month,
            paid_at__date__lt=current_month,
        ).aggregate(total=Sum("amount"))["total"] or 0

        customers = Accounts.objects.filter(
            is_staff=False,
            is_superuser=False,
        )

        current_customers = customers.filter(
            date_joined__date__gte=current_month,
            date_joined__date__lt=next_month,
        ).count()

        previous_customers = customers.filter(
            date_joined__date__gte=previous_month,
            date_joined__date__lt=current_month,
        ).count()

        return Response({
            "month": current_month.strftime("%Y-%m"),
            "total_bookings": current_bookings,
            "bookings_change": self.calculate_change(
                current_bookings,
                previous_bookings,
            ),
            "total_revenue": float(current_revenue),
            "revenue_change": self.calculate_change(
                current_revenue,
                previous_revenue,
            ),
            "active_rentals": bookings.filter(
                status__in=["confirmed", "picked_up"],
            ).count(),
            "customers": current_customers,
            "customers_change": self.calculate_change(
                current_customers,
                previous_customers,
            ),
        })


class AdminDashboardFleetStatusView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        cars = Cars.objects.all()
        total = cars.count()
        maintenance = cars.filter(status="maintenance").count()
        rented = cars.filter(
            status="available",
            bookings__status__in=["confirmed", "picked_up"],
        ).distinct().count()
        available = max(total - maintenance - rented, 0)

        def fleet_item(label, value):
            return {
                "label": label,
                "value": value,
                "percentage": round(value / total * 100) if total else 0,
            }

        return Response({
            "total": total,
            "items": [
                fleet_item("Available", available),
                fleet_item("Rented", rented),
                fleet_item("Maintenance", maintenance),
            ],
        })


class AdminDashboardRecentBookingsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        bookings = Booking.objects.select_related("user", "car")[:5]

        return Response({
            "bookings": [
                {
                    "booking_reference": booking.booking_reference,
                    "customer": (
                        booking.user.get_full_name()
                        or booking.user.email
                        or booking.user.username
                    ),
                    "vehicle": f"{booking.car.brand} {booking.car.model}",
                    "amount": float(booking.total_price),
                    "status": booking.status,
                    "status_label": booking.get_status_display(),
                }
                for booking in bookings
            ],
        })


class AdminDashboardAttentionView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            "items": [
                {
                    "label": "Pending approvals",
                    "description": "Bookings waiting for review",
                    "count": Booking.objects.filter(
                        status="pending_approval",
                    ).count(),
                    "route": "/admin/admin-booking",
                },
                {
                    "label": "Payment issues",
                    "description": "Transactions requiring attention",
                    "count": Payment.objects.filter(status="failed").count(),
                    "route": "/admin/admin-booking",
                },
                {
                    "label": "Vehicles in maintenance",
                    "description": "Cars currently unavailable",
                    "count": Cars.objects.filter(status="maintenance").count(),
                    "route": "/admin/admin-fleet",
                },
            ],
        })
