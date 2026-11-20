from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from ..models import AdminActivityLog, Booking, Notification, Payment, Refund
from ..serializers import TransactionSerializer
from ..utils.notifications import create_admin_notifications
from ..utils.refunds import create_pending_refund
from django.conf import settings
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from decimal import Decimal
import base64
import traceback
import requests


PAYMONGO_REFUND_STATUS_MAP = {
    "pending": "processing",
    "processing": "processing",
    "succeeded": "succeeded",
    "failed": "failed",
}


def _paymongo_headers():
    secret_key = getattr(settings, "PAYMONGO_SECRET_KEY", None)
    if not secret_key:
        return None
    encoded_key = base64.b64encode(f"{secret_key}:".encode()).decode()
    return {
        "Authorization": f"Basic {encoded_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _refund_error_message(payload):
    errors = payload.get("errors", []) if isinstance(payload, dict) else []
    if errors:
        detail = errors[0].get("detail") or errors[0].get("code")
        if detail:
            return str(detail)
    return "PayMongo could not process the refund."


def _notify_refund_status(refund, refund_status):
    booking = refund.payment.booking
    status_messages = {
        "processing": (
            "Refund Processing",
            f"Your refund for booking {booking.booking_reference} is being processed.",
        ),
        "succeeded": (
            "Refund Successful",
            f"Your refund for booking {booking.booking_reference} was successfully submitted.",
        ),
        "failed": (
            "Refund Failed",
            f"The refund for booking {booking.booking_reference} could not be processed. Drive Ease will review it.",
        ),
    }
    message = status_messages.get(refund_status)
    if not message:
        return

    Notification.objects.get_or_create(
        user_id=booking.user_id,
        deduplication_key=f"refund-{refund_status}:{refund.id}",
        defaults={
            "notification_type": "payment",
            "title": message[0],
            "message": message[1],
            "action_url": f"/client/transaction-details/{booking.booking_reference}",
            "booking": booking,
        },
    )
    create_admin_notifications(
        notification_type="payment",
        title=message[0],
        message=f"{message[1]} Amount: PHP {refund.amount}.",
        action_url="/admin/admin-booking",
        booking=booking,
        deduplication_key=f"admin-refund-{refund_status}:{refund.id}",
    )


def _apply_refund_provider_update(refund, provider_data):
    attributes = provider_data.get("attributes", {})
    provider_status = attributes.get("status", "processing")
    local_status = PAYMONGO_REFUND_STATUS_MAP.get(provider_status, "processing")

    with transaction.atomic():
        refund = Refund.objects.select_for_update().select_related(
            "payment__booking"
        ).get(pk=refund.pk)
        previous_status = refund.status
        refund.paymongo_refund_id = provider_data.get("id") or refund.paymongo_refund_id
        refund.status = local_status
        refund.paymongo_response = provider_data
        refund.failure_message = (
            _refund_error_message(provider_data) if local_status == "failed" else ""
        )
        if local_status == "succeeded":
            refund.processed_at = timezone.now()
        refund.save()

        payment = refund.payment
        if local_status == "succeeded":
            refunded_total = payment.refunds.filter(
                status="succeeded"
            ).aggregate(total=Sum("amount"))["total"] or Decimal("0")
            if refunded_total >= payment.amount and payment.status != "refunded":
                payment.status = "refunded"
                payment.save(update_fields=["status", "updated_at"])

        if previous_status != local_status:
            transaction.on_commit(
                lambda refund_id=refund.id, current_status=local_status:
                _notify_refund_status(
                    Refund.objects.select_related("payment__booking").get(pk=refund_id),
                    current_status,
                )
            )

    return refund

class CreatePayMongoPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        description = request.data.get('description')
        currency = request.data.get('currency', 'PHP')
        booking_reference = request.data.get('booking_reference')

        if not amount:
            return Response(
                {"error": "Amount is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not booking_reference:
            return Response(
                {"error": "Booking reference is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # PayMongo API credentials (should be in settings)
        paymongo_secret_key = getattr(settings, 'PAYMONGO_SECRET_KEY', None)
        if not paymongo_secret_key:
            return Response(
                {"error": "Payment gateway not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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

            booking = Booking.objects.filter(
                booking_reference=booking_reference,
                user=request.user,
            ).select_related("car").first()

            if not booking:
                return Response(
                    {"error": "Booking not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            car_reference = booking.car.car_reference

            success_url = (
                f"{settings.FRONTEND_URL}/client/car-details/{car_reference}"
                f"?payment=success&booking_reference={booking.booking_reference}"
            )

            cancel_url = (
                f"{settings.FRONTEND_URL}/client/car-details/{car_reference}"
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
                        "reference_number": booking.booking_reference,
                        "metadata": {
                            "booking_id": str(booking.id)
                        }
                    }
                }
            }

            response = requests.post(
                "https://api.paymongo.com/v2/checkout_sessions",
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
            # Checkout v2 creates the Payment Intent only when the customer
            # starts paying, so it may not exist in the create response yet.
            payment_intent = response_data["data"]["attributes"].get(
                "payment_intent"
            ) or {}
            payment_intent_id = payment_intent.get("id")
            checkout_url = response_data["data"]["attributes"]["checkout_url"]

            # Create Payment record
            Payment.objects.create(
                booking=booking,
                checkout_session_id=checkout_session_id,
                payment_intent_id=payment_intent_id,
                amount=int(amount) / 100,  # Convert back from centavos
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


class AdminIssueRefundView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, booking_reference):
        headers = _paymongo_headers()
        if not headers:
            return Response(
                {"message": "Payment gateway is not configured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        admin_note = str(request.data.get("note", "")).strip()
        if len(admin_note) > 255:
            return Response(
                {"note": "Refund notes cannot exceed 255 characters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            booking = get_object_or_404(
                Booking.objects.select_for_update(),
                booking_reference=booking_reference,
            )
            payment = Payment.objects.select_for_update().filter(
                booking=booking,
            ).first()

            if booking.status not in {"cancelled", "rejected"}:
                return Response(
                    {"message": "Only cancelled or rejected bookings can be refunded."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not payment or payment.status != "paid":
                return Response(
                    {"message": "Only paid bookings can be refunded."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not payment.paymongo_payment_id:
                return Response(
                    {
                        "message": (
                            "This payment was not processed through PayMongo and "
                            "must be refunded manually."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            existing = payment.refunds.filter(
                status__in={"processing", "succeeded"},
            ).first()
            if existing:
                message = (
                    "This payment has already been refunded."
                    if existing.status == "succeeded"
                    else "This refund is already being processed."
                )
                return Response(
                    {"message": message},
                    status=status.HTTP_409_CONFLICT,
                )

            refund = payment.refunds.filter(status="pending_review").first()
            if not refund:
                refund = Refund.objects.create(
                    payment=payment,
                    amount=payment.amount,
                    reason=(
                        "booking_rejected"
                        if booking.status == "rejected"
                        else "customer_cancellation"
                    ),
                    customer_reason=booking.cancel_reason,
                    requested_by=booking.user,
                )

            refund.status = "processing"
            refund.reviewed_by = request.user
            refund.admin_note = admin_note
            refund.failure_message = ""
            refund.save(update_fields=[
                "status",
                "reviewed_by",
                "admin_note",
                "failure_message",
                "updated_at",
            ])

        payload = {
            "data": {
                "attributes": {
                    "amount": int(refund.amount * 100),
                    "payment_id": payment.paymongo_payment_id,
                    "reason": "others",
                    "notes": admin_note or (
                        f"Full refund for booking {booking.booking_reference}"
                    ),
                }
            }
        }

        try:
            response = requests.post(
                "https://api.paymongo.com/v1/refunds",
                headers=headers,
                json=payload,
                timeout=30,
            )
            response_data = response.json()
        except requests.RequestException as exc:
            response_data = {
                "attributes": {"status": "failed"},
                "errors": [{"detail": str(exc)}],
            }
            _apply_refund_provider_update(refund, response_data)
            return Response(
                {"message": "PayMongo could not be reached. The refund was not completed."},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        except ValueError:
            response_data = {
                "attributes": {"status": "failed"},
                "errors": [{"detail": "PayMongo returned an invalid response."}],
            }
            _apply_refund_provider_update(refund, response_data)
            return Response(
                {"message": "PayMongo returned an invalid response."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        if not response.ok:
            failure_data = {
                "attributes": {"status": "failed"},
                "errors": response_data.get("errors", []),
            }
            _apply_refund_provider_update(refund, failure_data)
            return Response(
                {
                    "message": _refund_error_message(response_data),
                    "details": response_data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        provider_refund = response_data.get("data", {})
        refund = _apply_refund_provider_update(refund, provider_refund)

        AdminActivityLog.objects.create(
            admin=request.user,
            action="status_change",
            description=(
                f"Issued a full refund of PHP {refund.amount} for booking "
                f"{booking.booking_reference}."
            ),
            target_type="refund",
            target_id=refund.paymongo_refund_id or str(refund.id),
        )

        booking = Booking.objects.select_related("car", "user").get(pk=booking.pk)
        return Response(
            TransactionSerializer(booking).data,
            status=status.HTTP_200_OK,
        )

class PayMongoWebhookView(APIView):
    # PayMongo calls this endpoint directly, so it cannot provide a user JWT.
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            event_data = request.data.get("data", {})

            # PayMongo currently documents two webhook envelopes. Checkout v2
            # sends the event name in data.type, while the legacy event resource
            # places it in data.attributes.type. Normalize both to one shape.
            legacy_attributes = event_data.get("attributes", {})
            if legacy_attributes.get("type"):
                event_attributes = legacy_attributes
                event_type = event_attributes.get("type")
                event_resource = event_attributes.get("data", {})
            else:
                event_type = event_data.get("type")
                event_resource = event_data.get("data", {})

            # Handle successful Checkout v2 payment
            if event_type == "checkout_session.payment.paid":

                session = event_resource
                session_id = session.get("id")
                session_attributes = session.get("attributes", {})

                payments = session_attributes.get("payments", [])

                paid_payment = next(
                    (
                        payment for payment in payments
                        if payment.get("attributes", {}).get("status") == "paid"
                    ),
                    None
                )

                if not session_id or not paid_payment:
                    return Response(
                        {"error": "Missing checkout or payment information"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                payment_attributes = paid_payment.get("attributes", {})

                with transaction.atomic():

                    payment = Payment.objects.filter(
                        checkout_session_id=session_id
                    ).select_related("booking").first()

                    if not payment:
                        return Response(
                            {"error": "Payment record not found"},
                            status=status.HTTP_404_NOT_FOUND
                        )

                    booking = payment.booking
                    already_paid = payment.status == "paid"
                    provider_payment_id = paid_payment.get("id")

                    if (
                        provider_payment_id
                        and payment.paymongo_payment_id != provider_payment_id
                    ):
                        payment.paymongo_payment_id = provider_payment_id
                        payment.save(update_fields=[
                            "paymongo_payment_id",
                            "updated_at",
                        ])

                    if not already_paid:
                        booking_was_cancelled = booking.status == "cancelled"

                        # A delayed webhook must never reopen a booking that
                        # the customer has already cancelled.
                        if not booking_was_cancelled:
                            booking.status = "pending_approval"
                            booking.save(update_fields=["status"])

                        payment.status = "paid"
                        payment.paid_at = timezone.now()
                        payment.payment_intent_id = (
                            session_attributes.get("payment_intent", {}).get("id")
                        )
                        payment.payment_method = (
                            payment_attributes.get("source", {}).get("type")
                        )
                        payment.paymongo_payment_id = provider_payment_id
                        payment.paymongo_response = request.data

                        payment.save()

                        refund = None
                        refund_created = False
                        if booking_was_cancelled:
                            refund, refund_created = create_pending_refund(
                                payment=payment,
                                requested_by=booking.user,
                                customer_reason=booking.cancel_reason,
                            )

                        Notification.objects.create(
                            user_id=booking.user_id,
                            notification_type="payment",
                            title=(
                                "Payment Received After Cancellation"
                                if booking_was_cancelled else
                                "Booking Created"
                            ),
                            message=(
                                (
                                    f"Payment for cancelled booking "
                                    f"{booking.booking_reference} was received. "
                                    "Please contact Drive Ease for refund assistance."
                                )
                                if booking_was_cancelled else
                                (
                                    f"Your payment was successful. Booking "
                                    f"{booking.booking_reference} is now waiting "
                                    "for approval."
                                )
                            ),
                            action_url=(
                                "/client/transaction-details/"
                                f"{booking.booking_reference}"
                            ),
                            booking=booking,
                        )

                        transaction.on_commit(
                            lambda was_cancelled=booking_was_cancelled:
                            create_admin_notifications(
                                notification_type="payment",
                                title=(
                                    "Payment received for cancelled booking"
                                    if was_cancelled else
                                    "Payment received"
                                ),
                                message=(
                                    (
                                        f"Payment for cancelled booking "
                                        f"{booking.booking_reference} was received "
                                        "and may require a refund."
                                    )
                                    if was_cancelled else
                                    (
                                        f"Payment for booking "
                                        f"{booking.booking_reference} was received "
                                        "and is waiting for approval."
                                    )
                                ),
                                action_url="/admin/admin-booking",
                                booking=booking,
                                deduplication_key=f"payment-paid:{payment.id}",
                            )
                        )
                        if refund_created:
                            transaction.on_commit(
                                lambda refund_id=refund.id:
                                create_admin_notifications(
                                    notification_type="payment",
                                    title="Refund requires review",
                                    message=(
                                        f"Payment for cancelled booking "
                                        f"{booking.booking_reference} arrived after cancellation. "
                                        "Review its full refund."
                                    ),
                                    action_url="/admin/admin-booking",
                                    booking=booking,
                                    deduplication_key=f"refund-review:{refund_id}",
                                )
                            )

            # Reconcile refund changes, including refunds created in PayMongo's dashboard.
            elif event_type == "payment.refund.updated":
                refund_data = event_resource
                refund_attributes = refund_data.get("attributes", {})
                provider_refund_id = refund_data.get("id")
                provider_payment_id = refund_attributes.get("payment_id")

                refund = Refund.objects.filter(
                    paymongo_refund_id=provider_refund_id,
                ).select_related("payment__booking").first()

                if not refund and provider_payment_id:
                    payment = Payment.objects.filter(
                        paymongo_payment_id=provider_payment_id,
                    ).select_related("booking").first()
                    if payment:
                        refund, _ = Refund.objects.get_or_create(
                            paymongo_refund_id=provider_refund_id,
                            defaults={
                                "payment": payment,
                                "amount": Decimal(str(refund_attributes.get("amount", 0))) / 100,
                                "reason": refund_attributes.get("reason") or "others",
                                "status": "processing",
                                "paymongo_response": refund_data,
                            },
                        )

                if refund:
                    _apply_refund_provider_update(refund, refund_data)

            # Handle failed payment
            elif event_type == "payment.failed":

                payment_data = event_resource.get("attributes", {})

                metadata = payment_data.get("metadata", {})
                booking_id = metadata.get("booking_id")

                if booking_id:

                    with transaction.atomic():

                        booking = Booking.objects.filter(
                            id=booking_id
                        ).first()

                        if booking and booking.status != "cancelled":
                            
                            booking.status = "payment_failed"
                            booking.save(update_fields=["status"])

                            payment = Payment.objects.filter(
                                booking_id=booking_id
                            ).first()

                            if payment and payment.status != "failed":

                                payment.status = "failed"
                                payment.paymongo_response = request.data

                                payment.save(update_fields=[
                                    "status",
                                    "paymongo_response",
                                    "updated_at",
                                ])

                                event_id = event_data.get("id") or booking_id

                                transaction.on_commit(
                                    lambda: create_admin_notifications(
                                        notification_type="payment",
                                        title="Payment failed",
                                        message=(
                                            f"Payment for booking "
                                            f"{booking.booking_reference} failed "
                                            "and may require follow-up."
                                        ),
                                        action_url="/admin/admin-booking",
                                        booking=booking,
                                        deduplication_key=(
                                            f"payment-failed:{event_id}"
                                        ),
                                    )
                                )

            return Response(
                {"status": "success"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            traceback.print_exc()

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
