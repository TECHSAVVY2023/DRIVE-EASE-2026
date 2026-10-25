"""Uploads API views."""

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
