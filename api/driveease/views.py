from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes

from .models import ContactListModel, Cars, Reviews, ReviewHelpful, FileUploadModel, Booking, Payment
from .serializers import ContactListSerializer
from .forms import ContactListForm

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F
from django.db.models.fields import capfirst
from django.db.models import Avg, Count
from django.db.models import Case, When, Value, BooleanField
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
import traceback
import requests
import json

from .serializers import ReviewSerializer, CarSerializer, FileUploadSerializer, BookingSerializer, PaymentSerializer

# === Cars ===

class CarListView(APIView):
    def get(self, request):
        cars = Cars.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)
        
class CarDetailView(APIView):
    def get(self, request, car_id):
        car = Cars.objects.get(car_id=car_id)
        serializer = CarSerializer(car)
        return Response(serializer.data)

# === Reviews ===

class ReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Reviews.objects.all()

        rating = self.request.query_params.get("rating")
        if rating:
            queryset = queryset.filter(rating=rating)

        sort = self.request.query_params.get("sort")

        if sort == "highest":
            queryset = queryset.order_by("-helpful_count")
        elif sort == "lowest":
            queryset = queryset.order_by("helpful_count")
        elif sort == "newest":
            queryset = queryset.order_by("-created_at")
        else:
            queryset = queryset.order_by("created_at")

        return queryset

    def list(self, request, *args, **kwargs):
        # Unfiltered queryset for statistics
        stats_queryset = Reviews.objects.all()

        # Filtered queryset for displayed reviews
        queryset = self.get_queryset()

        avg_rating = stats_queryset.aggregate(
            avg_rating=Avg("rating")
        )["avg_rating"] or 0

        total_reviews = stats_queryset.count()

        rating_breakdown = {
            star: stats_queryset.filter(rating=star).count()
            for star in range(1, 6)
        }

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            response.data["avg_rating"] = round(avg_rating, 1)
            response.data["rating_breakdown"] = rating_breakdown
            response.data["total_reviews"] = total_reviews

            return response

class CarReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Reviews.objects.filter(
            car_id=self.kwargs["car_id"]
        )

        # Pin the current user's review
        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                is_mine=Case(
                    When(user=self.request.user, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
        else:
            queryset = queryset.annotate(
                is_mine=Value(False, output_field=BooleanField())
            )
        
        # Filter by rating
        rating = self.request.query_params.get("rating")
        if rating:
            queryset = queryset.filter(rating=rating)

        # Sort
        sort = self.request.query_params.get("sort")

        if sort == "highest":
            queryset = queryset.order_by("-helpful_count")
        elif sort == "lowest":
            queryset = queryset.order_by("helpful_count")
        elif sort == "newest":
            queryset = queryset.order_by("-created_at")
        else:
            queryset = queryset.order_by("created_at")

        return queryset

    def list(self, request, *args, **kwargs):
        all_reviews = Reviews.objects.filter(
            car_id=self.kwargs["car_id"]
        )

        queryset = self.get_queryset()

        avg_rating = all_reviews.aggregate(
            avg_rating=Avg("rating")
        )["avg_rating"] or 0

        total_reviews = all_reviews.count()

        breakdown = {
            star: all_reviews.filter(rating=star).count()
            for star in range(1, 6)
        }

        my_review = None

        if request.user.is_authenticated:
            my_review = queryset.filter(user=request.user).first()

            # Remove it from the normal review list
            if my_review:
                queryset = queryset.exclude(pk=my_review.pk)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            response = self.get_paginated_response(serializer.data)

            response.data["my_review"] = (
                self.get_serializer(my_review).data
                if my_review
                else None
            )

            response.data["total_reviews"] = total_reviews
            response.data["avg_rating"] = round(avg_rating, 1)
            response.data["rating_breakdown"] = breakdown

            return response

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "results": serializer.data,
            "my_review": (
                self.get_serializer(my_review).data
                if my_review
                else None
            ),
            "total_reviews": total_reviews,
            "avg_rating": round(avg_rating, 1),
            "rating_breakdown": breakdown,
        })

class FeaturedReviewsView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return (
            Reviews.objects
            .filter(images__isnull=False)
            .order_by('-helpful_count', '?')[:3]
        )
    
    def list(self, request, *args, **kwargs):
        # Unfiltered queryset for statistics
        stats_queryset = Reviews.objects.all()

        # Filtered queryset for displayed reviews
        queryset = self.get_queryset()

        avg_rating = stats_queryset.aggregate(
            avg_rating=Avg("rating")
        )["avg_rating"] or 0

        total_reviews = stats_queryset.count()

        rating_breakdown = {
            star: stats_queryset.filter(rating=star).count()
            for star in range(1, 6)
        }

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            response.data["avg_rating"] = round(avg_rating, 1)
            response.data["rating_breakdown"] = rating_breakdown
            response.data["total_reviews"] = total_reviews

            return response

class CreateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, car_id):
        car = Cars.objects.get(car_id=car_id)

        # Prevent duplicate reviews
        if Reviews.objects.filter(
            user=request.user,
            car=car
        ).exists():
            return Response(
                {"detail": "You have already reviewed this car."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rating = request.data.get("rating")
        text = request.data.get("review")
        images = request.data.get("images")

        review = Reviews.objects.create(
            user=request.user,
            car=car,
            rating=rating,
            text=text,
            images=images,
        )

        return Response(
            {
                "message": "Review submitted successfully.",
                "review_id": review.id
            },
            status=status.HTTP_201_CREATED,
        )

class UpdateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, car_id, review_id):
        try:
            review = Reviews.objects.get(
                id=review_id,
                user=request.user,
                car=car_id
            )
        except Reviews.DoesNotExist:
            return Response(
                {"detail": "Review not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data

        review.rating = data.get("rating", review.rating)
        review.text = data.get("review", review.text)
        review.images = data.get("images", review.images)

        # Images that should remain after editing
        existing_images = data.get("images", [])

        # Images the frontend explicitly removed
        deleted_images = data.get("deleted_images", [])


        for upload in FileUploadModel.objects.all():

            if upload.file and upload.file.url in deleted_images:
                upload.file.delete(save=False)
                upload.delete()

        review.save()

        return Response(
            {
                "message": "Review updated successfully.",
                "review_id": review.id,
            },
            status=status.HTTP_200_OK,
        )

class DeleteReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, car_id, review_id):
        try:
            review = Reviews.objects.get(
                id=review_id,
                user=request.user,
                car=car_id
            )
        except Reviews.DoesNotExist:
            return Response(
                {"detail": "Review not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Delete associated uploaded images
        for image_url in review.images or []:
            for upload in FileUploadModel.objects.all():
                if upload.file and upload.file.url == image_url:
                    upload.file.delete(save=False)
                    upload.delete()

        # Delete the review
        review.delete()

        return Response(
            {"message": "Review deleted successfully."},
            status=status.HTTP_200_OK,
        )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_helpful(request, review_id):
    review = get_object_or_404(Reviews, pk=review_id)

    with transaction.atomic():

        vote, created = ReviewHelpful.objects.get_or_create(
            review=review,
            user=request.user
        )

        if created:
            Reviews.objects.filter(pk=review.pk).update(
                helpful_count=F("helpful_count") + 1
            )

            helpful = True

        else:
            vote.delete()

            Reviews.objects.filter(pk=review.pk).update(
                helpful_count=F("helpful_count") - 1
            )

            helpful = False

    review.refresh_from_db(fields=["helpful_count"])

    return Response({
        "helpful": helpful,
        "helpful_count": review.helpful_count
    })

# === Contact ===

class ContactListView(APIView):
  def get(self, request, format=None):
    obj = ContactListModel.objects.all()
    serializer = ContactListSerializer(obj, many=True)
    
    return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class ContactCreateView(APIView):
  def post(self, request):
    form = ContactListForm(request.data)

    if form.is_valid():
      obj = form.save(commit=False)
      obj.save()

      return Response({'status':'created'})
    else:
      return Response({'status':'errors', 'errors': form.errors})
  
  def put(self, request, pk):
    obj = ContactListModel.objects.get(pk=pk)
    form = ContactListForm(request.data, instance=obj)
    form.save()

    return Response({'status': 'updated'})

  def delete(self, request, pk):
    obj = ContactListModel.objects.get(pk=pk)
    obj.delete()

    return Response({'status': 'deleted'})
  
class ContactDetailView(APIView):
  def get(self, request, pk, format=None):
    obj = ContactListModel.objects.get(pk=pk)
    serializer = ContactListSerializer(obj)

    return Response(serializer.data)
  
@method_decorator(csrf_exempt, name='dispatch')
class SubmitToGmail(APIView):
  def post(self, request):
    try:
      form = ContactListForm(request.data)

      if not form.is_valid():
        return Response({
          'status': 'error',
          'message': 'Invalid form data',
          'errors': form.errors
        }, status=status.HTTP_400_BAD_REQUEST)

      # Build context after validation
      context = {
        "contact_id": form.cleaned_data.get('contact_id'),
        "firstname": form.cleaned_data.get('firstname'),
        "lastname": form.cleaned_data.get('lastname'),
        "contact_email": form.cleaned_data.get('contact_email'),
        "contact_number": form.cleaned_data.get('contact_number'),
        "message": form.cleaned_data.get('message'),
        "timestamp": timezone.localtime(timezone.now()).strftime("%B %d, %Y at %I:%M %p"),
      }

      firstname = form.cleaned_data.get('firstname')
      lastname = form.cleaned_data.get('lastname')
      recipient_email = form.cleaned_data.get('contact_email')

      # Subject lines
      subject_inquiry = f"Inquiry from {firstname} {lastname}"
      subject_thankyou = "Thank You for Contacting DriveEase"

      # Render HTML templates
      html_message_inquiry = render_to_string('contact.html', context)
      plain_message_inquiry = strip_tags(html_message_inquiry)

      html_message_thankyou = render_to_string('thankyou.html', context)
      plain_message_thankyou = strip_tags(html_message_thankyou)

      # Internal team recipients
      internal_recipients = [
        'zrephy08@gmail.com',
      ]

      try:
        # Send inquiry email to team
        mail.send_mail(
          subject_inquiry,
          plain_message_inquiry,
          'zrephy08@gmail.com',  # Use proper from email
          internal_recipients,
          html_message=html_message_inquiry,
          fail_silently=False
        )

        # Send thank-you email to inquirer
        mail.send_mail(
          subject_thankyou,
          plain_message_thankyou,
          'DriveEase <zrephy08@gmail.com>',  # Use proper from email
          [recipient_email],
          html_message=html_message_thankyou,
          fail_silently=False
        )

        return Response({'status': 'sent'}, status=status.HTTP_200_OK)

      except Exception as email_error:
        print(f"Email sending error: {email_error}")
        traceback.print_exc()
        return Response({
          'status': 'error',
          'message': 'Failed to send email notifications'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
      print(f"General error in SubmitToGmail: {e}")
      traceback.print_exc()
      return Response({
        'status': 'error',
        'message': 'Internal server error'
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# === File Upload ===

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FileUploadSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        upload = serializer.save()

        return Response({
            "id": upload.id,
            "url": upload.file.url
        })

# === Bookings ===

class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Generate booking reference if not provided
        if not serializer.validated_data.get('booking_reference'):
            import uuid
            serializer.validated_data['booking_reference'] = f'BKG-{uuid.uuid4().hex[:10].upper()}'
        
        booking = serializer.save()
        
        return Response({
            "message": "Booking created successfully.",
            "booking_id": booking.id,
            "booking_reference": booking.booking_reference
        }, status=status.HTTP_201_CREATED)

# === Payments ===

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

            checkout_url = response_data['data']['attributes']['checkout_url']
            payment_intent_id = response_data['data']['id']

            # Create Payment record
            booking = Booking.objects.filter(id=booking_id).first()
            if booking:
                Payment.objects.create(
                    booking=booking,
                    checkout_session_id=payment_intent_id,
                    payment_intent_id=payment_intent_id,
                    amount=amount / 100,  # Convert back from cents
                    currency=currency,
                    status='pending',
                    paymongo_response=response_data
                )

            return Response({
                'checkout_url': checkout_url,
                'payment_intent_id': payment_intent_id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Webhook handler - Commented out for development
# Uncomment when ready to implement webhooks with ngrok or production deployment
class PayMongoWebhookView(APIView):
    def post(self, request):
        from django.conf import settings
        import hmac
        import hashlib

        print("=" * 60)
        print("PAYMONGO WEBHOOK RECEIVED")
        print("=" * 60)

        print("Headers:")
        print(dict(request.headers))

        print("\nBody:")
        print(json.dumps(request.data, indent=4))

        print("=" * 60)
        
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
            print(f"Event Type: {event_type}")
            
            # Handle payment success
            if event_type == 'payment.paid':
                payment_data = attributes.get('data', {}).get('attributes', {})
                metadata = payment_data.get('metadata', {})
                booking_id = metadata.get('booking_id')
                print(f"Booking ID: {booking_id}")
                
                if booking_id:
                    # Update booking status to confirmed
                    booking = Booking.objects.filter(id=booking_id).first()
                    if booking:
                        print(f"Updating Booking #{booking.id} -> confirmed")
                        booking.status = 'confirmed'
                        booking.save()
                    
                    # Update payment status and set paid_at
                    payment = Payment.objects.filter(booking_id=booking_id).first()
                    if payment:
                        print(f"Updating Payment #{payment.id} -> paid")
                        payment.status = 'paid'
                        payment.paid_at = timezone.now()
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
