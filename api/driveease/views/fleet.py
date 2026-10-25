"""Fleet API views."""

from django.db import transaction
from django.db.models import Count, Exists, OuterRef, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..filter_options import get_filter_options
from ..models import AdminActivityLog, Booking, Cars, CarType, Feature, FileUploadModel
from ..pagination import FleetPagination
from ..serializers import (
    CarCreateSerializer,
    CarSerializer,
    CarTypeSerializer,
    CarUpdateSerializer,
    FeatureSerializer,
)

class CarListView(APIView):
    def get(self, request):
        cars = Cars.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)


class FleetListView(ListAPIView):
    serializer_class = CarSerializer
    pagination_class = FleetPagination

    def get_queryset(self):
        queryset = Cars.objects.all()

        # Search
        search = self.request.query_params.get("search")
        
        if search:
            search_terms = search.split()

            for term in search_terms:
                queryset = queryset.filter(
                    Q(brand__icontains=term) |
                    Q(model__icontains=term)
                )

        # Condition
        status = self.request.query_params.get("status")

        if status == "available":
            queryset = queryset.filter(status="available")

        elif status == "maintenance":
            queryset = queryset.filter(status="maintenance")

        # Filter by transmission
        transmission = self.request.query_params.get("transmission")
        if transmission:
            transmissions = [
                item.strip()
                for item in transmission.split(",")
            ]

            queryset = queryset.filter(
                transmission__in=transmissions
            )

        # Filter by seats
        seat_param = self.request.query_params.get("seats")
        if seat_param:
            selected_seats = [
                item.strip()
                for item in seat_param.split(",")
            ]

            queryset = queryset.filter(
                seats__in=selected_seats
            )

        # Filter by fuel type
        fuel = self.request.query_params.get("fuel_type")
        if fuel:
            selected_fuel = [
                item.strip()
                for item in fuel.split(",")
            ]

            queryset = queryset.filter(
                fuel_type__in=selected_fuel
            )

        # Filter by car type
        car_type = self.request.query_params.get("car_type")

        if car_type:
            car_type_ids = [
                int(item.strip())
                for item in car_type.split(",")
                if item.strip()
            ]

            queryset = queryset.filter(
                car_type_id__in=car_type_ids
            )

        # Filter by features
        features = self.request.query_params.get("features")
        if features:
            feature_list = [
                item.strip()
                for item in features.split(",")
            ]

            queryset = queryset.filter(
                features__name__in=feature_list
            ).distinct()

        # Filter by price range
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if min_price:
            queryset = queryset.filter(price_per_day__gte=min_price)

        if max_price:
            queryset = queryset.filter(price_per_day__lte=max_price)

        # Check for currently rented cars
        active_bookings = Booking.objects.filter(
            car=OuterRef("pk"),
            status__in=[
                "pending_approval",
                "confirmed",
                "picked_up",
            ],
            return_date__gt=timezone.now(),
        )

        queryset = queryset.annotate(
            has_active_booking=Exists(active_bookings),
            rental_count=Count(
                "bookings",
                filter=Q(
                    bookings__status__in=[
                        "picked_up",
                        "returned",
                        "completed",
                    ]
                ),
                distinct=True,
            ),
        )

        # Sort
        sort = self.request.query_params.get("sort")
        prioritize_available = (
            self.request.query_params.get("prioritize_available") == "true"
        )

        if sort == "price-asc":
            if prioritize_available:
                queryset = queryset.order_by(
                    "has_active_booking",
                    "price_per_day",
                )
            else:
                queryset = queryset.order_by(
                    "price_per_day",
                )

        elif sort == "price-desc":
            if prioritize_available:
                queryset = queryset.order_by(
                    "has_active_booking",
                    "-price_per_day",
                )
            else:
                queryset = queryset.order_by(
                    "-price_per_day",
                )

        elif sort == "name":
            if prioritize_available:
                queryset = queryset.order_by(
                    "has_active_booking",
                    "brand",
                    "model",
                )
            else:
                queryset = queryset.order_by(
                    "brand",
                    "model",
                )

        else:
            if prioritize_available:
                queryset = queryset.order_by(
                    "has_active_booking",
                )
            else:
                queryset = queryset.order_by(
                    "brand",
                    "model",
                )
            
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            paginated_response = self.get_paginated_response(serializer.data)

            paginated_response.data["filters"] = get_filter_options()

            return paginated_response

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "results": serializer.data,
            "filters": get_filter_options(),
        })


class CarDetailView(APIView):
    def get(self, request, car_id):
        car = Cars.objects.get(car_id=car_id)
        serializer = CarSerializer(car)
        return Response(serializer.data)


class FleetStatsView(APIView):

    def get(self, request):
        total_cars = Cars.objects.count()
        maintenance_count = Cars.objects.filter(status="maintenance").count()

        pending_approval_count = Booking.objects.filter(
            status="pending_approval"
        ).values("car_id").distinct().count()

        available_count = Cars.objects.filter(
            status="available"
        ).exclude(
            bookings__status__in=[
                "pending_payment",
                "pending_approval",
                "confirmed",
                "picked_up",
            ]
        ).distinct().count()

        unavailable_count = total_cars - available_count - maintenance_count

        rented_count = Booking.objects.filter(
            status__in=[
                "confirmed",
                "pending_approval",
                "picked_up",
            ]
        ).values("car_id").distinct().count()

        fleet_condition = (
            round((total_cars - maintenance_count) / total_cars * 100)
            if total_cars else 0
        )

        available_percentage = (
            round(available_count / total_cars * 100)
            if total_cars else 0
        )

        return Response({
            "total_cars": total_cars,
            "available_count": available_count,
            "unavailable_count": unavailable_count,
            "maintenance_count": maintenance_count,
            "pending_approval_count": pending_approval_count,
            "fleet_condition": fleet_condition,
            "available_percentage": available_percentage,
            "rented_count": rented_count,
        })


class CarCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CarCreateSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            car = serializer.save()

            AdminActivityLog.objects.create(
                admin=request.user,
                action="create",
                description=f"Added car {car.brand} {car.model}.",
                target_type="car",
                target_id=str(car.car_id),
            )

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class CarTypeListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        car_types = CarType.objects.all()
        serializer = CarTypeSerializer(car_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarTypeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class FeatureListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        features = Feature.objects.all()
        serializer = FeatureSerializer(features, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FeatureSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CarUpdateView(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def patch(self, request, car_id):
        car = get_object_or_404(Cars, car_id=car_id)

        old_meta = car.meta or {}
        old_image_urls = {
            url for url in [
                old_meta.get("primary_image"),
                *(old_meta.get("images") or []),
            ]
            if url
        }

        deleted_images = request.data.get("deleted_images", [])

        if not isinstance(deleted_images, list):
            return Response(
                {"deleted_images": "Expected a list of URLs."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invalid_urls = [
            url for url in deleted_images
            if url not in old_image_urls
        ]

        if invalid_urls:
            return Response(
                {
                    "deleted_images": (
                        "One or more selected images do not belong "
                        "to this vehicle."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CarUpdateSerializer(
            car,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Delete matching files from cloud storage and FileUploadModel.
        for upload in FileUploadModel.objects.exclude(file=""):
            if upload.file.url in deleted_images:
                upload.file.delete(save=False)
                upload.delete()

        AdminActivityLog.objects.create(
            admin=request.user,
            action="update",
            description=f"Updated car {car.brand} {car.model}.",
            target_type="car",
            target_id=str(car.car_id),
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CarDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, car_id):
        car = get_object_or_404(Cars, car_id=car_id)

        car.delete()

        AdminActivityLog.objects.create(
            admin=request.user,
            action="delete",
            description=f"Deleted car {car.brand} {car.model}.",
            target_type="car",
            target_id=str(car.car_id),
        )

        return Response(
            {"message": "Car deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
