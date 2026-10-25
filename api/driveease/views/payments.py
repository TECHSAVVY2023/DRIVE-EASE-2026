"""Payments API views."""

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

class CreatePayMongoPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from django.conf import settings
        import base64
        
        amount = request.data.get('amount')
        description = request.data.get('description')
        currency = request.data.get('currency', 'PHP')
        booking_id = request.data.get('booking_id')

        if not amount:
            return Response(
                {"error": "Amount is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not booking_id:
            return Response(
                {"error": "Booking ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # PayMongo API credentials (should be in settings)
        paymongo_secret_key = getattr(settings, 'PAYMONGO_SECRET_KEY', None)
        if not paymongo_secret_key:
            return Response(
                {"error": "Payment gateway not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        print(repr(paymongo_secret_key))
        try:
            # Create PayMongo checkout session
            encoded_key = base64.b64encode(
                f"{paymongo_secret_key}:".encode()
            ).decode()

            headers = {
                "Authorization": f"Basic {encoded_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            booking = Booking.objects.filter(id=booking_id).select_related("car").first()

            if not booking:
                return Response(
                    {"error": "Booking not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            car_id = booking.car.car_id   # or booking.car.id

            success_url = (
                f"{settings.FRONTEND_URL}/client/car-details/{car_id}"
                f"?payment=success&booking_id={booking_id}"
            )

            cancel_url = (
                f"{settings.FRONTEND_URL}/client/car-details/{car_id}"
                f"?payment=cancelled"
            )

            checkout_data = {
                "data": {
                    "attributes": {
                        "line_items": [
                            {
                                "currency": currency,
                                "amount": int(amount),  # Amount in centavos
                                "name": "DriveEase Car Rental",
                                "quantity": 1,
                                "description": description,
                            }
                        ],
                        "payment_method_types": [
                            "gcash",
                            "paymaya",
                            "card"
                        ],
                        "success_url": success_url,
                        "cancel_url": cancel_url,
                        "send_email_receipt": True,
                        "metadata": {
                            "booking_id": booking_id
                        }
                    }
                }
            }

            response = requests.post(
                "https://api.paymongo.com/v1/checkout_sessions",
                headers=headers,
                json=checkout_data,
            )

            response_data = response.json()

            if not response.ok:
                return Response(
                    {"error": "Failed to create payment session", "details": response_data},
                    status=status.HTTP_400_BAD_REQUEST
                )

            checkout_session_id = response_data["data"]["id"]
            payment_intent_id = response_data["data"]["attributes"]["payment_intent"]["id"]
            checkout_url = response_data["data"]["attributes"]["checkout_url"]

            # Create Payment record
            booking = Booking.objects.filter(id=booking_id).first()
            if booking:
                Payment.objects.create(
                    booking=booking,
                    checkout_session_id=checkout_session_id,
                    payment_intent_id=payment_intent_id,
                    amount=amount / 100,  # Convert back from cents
                    currency=currency,
                    status='pending',
                    paymongo_response=response_data
                )

            return Response({
                'checkout_url': checkout_url,
                'checkout_session_id': checkout_session_id,
                'payment_intent_id': payment_intent_id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PayMongoWebhookView(APIView):
    def post(self, request):
        from django.conf import settings
        import hmac
        import hashlib

        print("PAYMONGO WEBHOOK RECEIVED")

        # print("Headers:")
        # print(dict(request.headers))

        # print("\nBody:")
        # print(json.dumps(request.data, indent=4))

        # print("=" * 60)
        
        # Get PayMongo webhook secret from settings
        # webhook_secret = getattr(settings, 'PAYMONGO_WEBHOOK_SECRET', None)
        
        # # Verify webhook signature if secret is configured
        # if webhook_secret:
        #     signature = request.headers.get('Paymongo-Signature', '')
        #     if not signature:
        #         return Response(
        #             {"error": "Missing signature"},
        #             status=status.HTTP_400_BAD_REQUEST
        #         )
            
            # Verify signature (implementation depends on PayMongo's signature format)
            # This is a basic verification - you may need to adjust based on PayMongo docs
        
        try:
            data = request.data.get('data', {})
            attributes = data.get('attributes', {})
            event_type = attributes.get('type')
            
            # Handle payment success
            if event_type == 'payment.paid':
                payment_data = attributes.get('data', {}).get('attributes', {})

                print(json.dumps(payment_data, indent=4))

                metadata = payment_data.get('metadata', {})
                booking_id = metadata.get('booking_id')
                
                if booking_id:
                    # Update booking status to confirmed
                    booking = Booking.objects.filter(id=booking_id).first()
                    if booking:
                        booking.status = "pending_approval"
                        booking.save()
                    
                    # Update payment status and set paid_at
                    payment = Payment.objects.filter(booking_id=booking_id).first()
                    if payment:
                        payment.status = "paid"
                        payment.paid_at = timezone.now()
                        payment.payment_method = payment_data.get("source", {}).get("type")
                        payment.paymongo_response = request.data
                        payment.save()
            
            # Handle payment failure
            elif event_type == 'payment.failed':
                payment_data = attributes.get('data', {}).get('attributes', {})
                metadata = payment_data.get('metadata', {})
                booking_id = metadata.get('booking_id')
                
                if booking_id:
                    # Update booking status to payment_failed
                    booking = Booking.objects.filter(id=booking_id).first()
                    if booking:
                        print(f"Updating Booking #{booking.id} -> payment_failed")
                        booking.status = 'payment_failed'
                        booking.save()
            
            return Response({"status": "success"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            traceback.print_exc()
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
