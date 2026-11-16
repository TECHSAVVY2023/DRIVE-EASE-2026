from django.urls import reverse
from django.conf import settings
from django.core.management import call_command
from django.utils import timezone
from datetime import timedelta
from io import StringIO
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Accounts,
    AdminActivityLog,
    Booking,
    CarAvailabilityAlert,
    Cars,
    CarType,
    Notification,
    Payment,
    Refund,
)
from .utils.notifications import (
    create_admin_notifications,
    create_due_car_availability_notifications,
)


class CarAvailabilityAlertTests(APITestCase):
    def setUp(self):
        self.user = Accounts.objects.create_user(
            username="availability-user@example.com",
            email="availability-user@example.com",
            password="test-password",
        )
        self.car_type = CarType.objects.create(name="Sedan", slug="sedan")
        self.car = Cars.objects.create(
            brand="Toyota",
            model="Vios",
            year=2026,
            car_type=self.car_type,
            price_per_day=2000,
            transmission="Automatic",
            engine="1.5L",
            fuel_type="Gasoline",
            seats=5,
            status="available",
        )
        self.booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            pickup_date=timezone.now() - timedelta(hours=1),
            return_date=timezone.now() + timedelta(hours=2),
            pickup_location="Cagayan de Oro",
            return_location="Cagayan de Oro",
            daily_rate=2000,
            number_of_days=1,
            subtotal=2000,
            discount=0,
            total_price=2000,
            status="picked_up",
        )
        self.url = reverse(
            "car-availability-alert",
            kwargs={"car_reference": self.car.car_reference},
        )

    def test_customer_can_subscribe_only_once(self):
        self.client.force_authenticate(self.user)

        first_response = self.client.post(self.url, {}, format="json")
        second_response = self.client.post(self.url, {}, format="json")

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            CarAvailabilityAlert.objects.filter(
                user=self.user,
                car=self.car,
            ).count(),
            1,
        )

    def test_alert_creates_one_notification_when_rental_ends(self):
        alert = CarAvailabilityAlert.objects.create(
            user=self.user,
            car=self.car,
        )
        self.booking.status = "returned"
        self.booking.save()

        created = create_due_car_availability_notifications(
            user=self.user,
        )

        self.assertEqual(created, 1)
        self.assertFalse(
            CarAvailabilityAlert.objects.filter(pk=alert.pk).exists()
        )
        notification = Notification.objects.get(user=self.user)
        self.assertEqual(notification.title, "Car Now Available")
        self.assertEqual(
            notification.action_url,
            f"/client/car-details/{self.car.car_reference}",
        )


class AssignAccountRoleTests(APITestCase):
    def setUp(self):
        self.admin = Accounts.objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            password="test-password",
            is_staff=True,
        )
        self.user = Accounts.objects.create_user(
            username="user@example.com",
            email="user@example.com",
            password="test-password",
        )
        self.url = reverse(
            "account-assign-role",
            kwargs={"user_reference": self.user.user_reference},
        )

    def test_regular_admin_cannot_assign_admin_role(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {"role": "Admin"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_regular_user_cannot_assign_roles(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            reverse(
                "account-assign-role",
                kwargs={"user_reference": self.admin.user_reference},
            ),
            {"role": "Customer"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_admin_cannot_assign_super_admin_role(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            self.url,
            {"role": "Super Admin"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_super_admin_can_assign_super_admin_role(self):
        super_admin = Accounts.objects.create_superuser(
            username="owner@example.com",
            email="owner@example.com",
            password="test-password",
        )
        self.client.force_authenticate(super_admin)

        response = self.client.patch(
            self.url,
            {"role": "Super Admin"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)

    def test_admin_cannot_change_own_role(self):
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            reverse(
                "account-assign-role",
                kwargs={"user_reference": self.admin.user_reference},
            ),
            {"role": "Customer"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class AdminCreateAccountTests(APITestCase):
    def setUp(self):
        self.admin = Accounts.objects.create_user(
            username="admin-create@example.com",
            email="admin-create@example.com",
            password="test-password",
            is_staff=True,
        )
        self.url = reverse("admin-create-account")
        self.payload = {
            "given_name": "New",
            "family_name": "User",
            "email": "NEW.USER@GMAIL.COM",
            "contact_number": "09123456789",
            "address": "Cebu City",
            "id_images": {
                "images": [
                    "https://example.com/id-front.jpg",
                    "https://example.com/id-back.jpg",
                ]
            },
            "role": "Customer",
        }

    def test_admin_can_create_google_only_user(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        account = Accounts.objects.get(email="new.user@gmail.com")
        self.assertEqual(account.username, "new.user@gmail.com")
        self.assertFalse(account.has_usable_password())
        self.assertFalse(account.is_staff)
        self.assertEqual(len(account.id_images["images"]), 2)
        self.assertTrue(
            AdminActivityLog.objects.filter(
                admin=self.admin,
                action="create",
                target_id=account.user_reference,
            ).exists()
        )

    def test_duplicate_email_is_rejected_case_insensitively(self):
        Accounts.objects.create_user(
            username="new.user@gmail.com",
            email="new.user@gmail.com",
        )
        self.client.force_authenticate(self.admin)
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_regular_admin_cannot_create_super_admin(self):
        self.client.force_authenticate(self.admin)
        self.payload["role"] = "Super Admin"
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(
            Accounts.objects.filter(email="new.user@gmail.com").exists()
        )

    def test_regular_admin_cannot_create_admin(self):
        self.client.force_authenticate(self.admin)
        self.payload["role"] = "Admin"
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(
            Accounts.objects.filter(email="new.user@gmail.com").exists()
        )

    def test_super_admin_can_create_admin(self):
        super_admin = Accounts.objects.create_superuser(
            username="creator-owner@example.com",
            email="creator-owner@example.com",
            password="test-password",
        )
        self.client.force_authenticate(super_admin)
        self.payload["role"] = "Admin"
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        account = Accounts.objects.get(email="new.user@gmail.com")
        self.assertTrue(account.is_staff)
        self.assertFalse(account.is_superuser)

    def test_admin_can_create_customer_without_ids(self):
        self.client.force_authenticate(self.admin)
        self.payload["id_images"] = {"images": []}
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        account = Accounts.objects.get(email="new.user@gmail.com")
        self.assertEqual(account.id_images, {"images": []})

    def test_more_than_five_ids_is_rejected(self):
        self.client.force_authenticate(self.admin)
        self.payload["id_images"] = {
            "images": [
                f"https://example.com/id-{index}.jpg"
                for index in range(6)
            ]
        }
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AdminAccountActionsTests(APITestCase):
    def setUp(self):
        self.admin = Accounts.objects.create_user(
            username="actions-admin@example.com",
            email="actions-admin@example.com",
            password="test-password",
            is_staff=True,
        )
        self.user = Accounts.objects.create_user(
            username="actions-user@example.com",
            email="actions-user@example.com",
            password="test-password",
        )
        self.client.force_authenticate(self.admin)

    def test_admin_can_suspend_and_activate_user(self):
        url = reverse(
            "account-update-status",
            kwargs={"user_reference": self.user.user_reference},
        )
        suspended = self.client.patch(
            url, {"is_active": False}, format="json"
        )
        self.assertEqual(suspended.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

        activated = self.client.patch(
            url, {"is_active": True}, format="json"
        )
        self.assertEqual(activated.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_admin_can_delete_user(self):
        reference = self.user.user_reference
        response = self.client.delete(
            reverse(
                "admin-edit-account",
                kwargs={"user_reference": reference},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Accounts.objects.filter(pk=self.user.pk).exists())
        self.assertTrue(
            AdminActivityLog.objects.filter(
                admin=self.admin,
                action="delete",
                target_id=reference,
            ).exists()
        )

    def test_admin_cannot_delete_own_account(self):
        response = self.client.delete(
            reverse(
                "admin-edit-account",
                kwargs={"user_reference": self.admin.user_reference},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Accounts.objects.filter(pk=self.admin.pk).exists())

    def test_regular_admin_cannot_manage_another_admin(self):
        other_admin = Accounts.objects.create_user(
            username="other-admin@example.com",
            email="other-admin@example.com",
            is_staff=True,
        )

        edit_response = self.client.patch(
            reverse(
                "admin-edit-account",
                kwargs={"user_reference": other_admin.user_reference},
            ),
            {"given_name": "Changed"},
            format="json",
        )
        status_response = self.client.patch(
            reverse(
                "account-update-status",
                kwargs={"user_reference": other_admin.user_reference},
            ),
            {"is_active": False},
            format="json",
        )
        delete_response = self.client.delete(
            reverse(
                "admin-edit-account",
                kwargs={"user_reference": other_admin.user_reference},
            )
        )

        self.assertEqual(edit_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(status_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)


class ClientBookingAvailabilityTests(APITestCase):
    def setUp(self):
        self.first_customer = Accounts.objects.create_user(
            username="first-booking-customer@example.com",
            email="first-booking-customer@example.com",
            password="test-password",
        )
        self.second_customer = Accounts.objects.create_user(
            username="second-booking-customer@example.com",
            email="second-booking-customer@example.com",
            password="test-password",
            id_images={"images": ["https://example.com/valid-id.jpg"]},
        )
        car_type = CarType.objects.create(name="Booking Sedan", slug="booking-sedan")
        self.car = Cars.objects.create(
            brand="Honda",
            model="City",
            year=2026,
            car_type=car_type,
            price_per_day=1800,
            transmission="Automatic",
            engine="1.5L",
            fuel_type="Gasoline",
            seats=5,
        )
        self.pickup_date = timezone.now() + timedelta(days=2)
        self.return_date = self.pickup_date + timedelta(days=2)
        self.hold = Booking.objects.create(
            user=self.first_customer,
            car=self.car,
            pickup_date=self.pickup_date,
            return_date=self.return_date,
            pickup_location="Cagayan de Oro",
            return_location="Cagayan de Oro",
            daily_rate=1800,
            number_of_days=2,
            subtotal=3600,
            discount=0,
            total_price=3600,
            status="pending_payment",
        )
        self.client.force_authenticate(self.second_customer)

    def booking_payload(self):
        return {
            "user_reference": self.second_customer.user_reference,
            "car_reference": self.car.car_reference,
            "pickup_date": self.pickup_date.isoformat(),
            "return_date": self.return_date.isoformat(),
            "pickup_location": "Cagayan de Oro",
            "return_location": "Cagayan de Oro",
            "daily_rate": 1800,
            "number_of_days": 2,
            "subtotal": 3600,
            "discount": 0,
            "total_price": 3600,
        }

    def test_recent_pending_payment_booking_holds_selected_dates(self):
        response = self.client.post(
            reverse("create-booking"),
            self.booking_payload(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("temporarily held", response.data["message"])
        self.assertEqual(Booking.objects.filter(car=self.car).count(), 1)

    def test_booking_requires_at_least_one_id_image(self):
        self.second_customer.id_images = {"images": []}
        self.second_customer.save(update_fields=["id_images"])

        response = self.client.post(
            reverse("create-booking"),
            self.booking_payload(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("at least one valid ID", response.data["id_images"])

    @patch("driveease.views.bookings.create_notification.delay")
    def test_expired_pending_payment_hold_releases_selected_dates(self, notification_delay):
        Booking.objects.filter(pk=self.hold.pk).update(
            created_at=timezone.now() - timedelta(minutes=16),
        )

        response = self.client.post(
            reverse("create-booking"),
            self.booking_payload(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.filter(car=self.car).count(), 2)
        notification_delay.assert_not_called()


class ClientBookingCancellationTests(APITestCase):
    def setUp(self):
        self.customer = Accounts.objects.create_user(
            username="cancel-customer@example.com",
            email="cancel-customer@example.com",
            password="test-password",
        )
        self.other_customer = Accounts.objects.create_user(
            username="other-customer@example.com",
            email="other-customer@example.com",
            password="test-password",
        )
        self.admin = Accounts.objects.create_user(
            username="cancel-admin@example.com",
            email="cancel-admin@example.com",
            password="test-password",
            is_staff=True,
        )
        car_type = CarType.objects.create(
            name="Cancellation Sedan",
            slug="cancellation-sedan",
        )
        self.car = Cars.objects.create(
            brand="Toyota",
            model="Altis",
            year=2026,
            car_type=car_type,
            price_per_day=2000,
            transmission="Automatic",
            engine="1.8L",
            fuel_type="Gasoline",
            seats=5,
        )
        self.booking = Booking.objects.create(
            user=self.customer,
            car=self.car,
            pickup_date=timezone.now() + timedelta(days=3),
            return_date=timezone.now() + timedelta(days=5),
            daily_rate=2000,
            number_of_days=2,
            subtotal=4000,
            discount=0,
            total_price=4000,
            status="pending_approval",
        )
        self.url = reverse(
            "booking-cancel",
            kwargs={"booking_reference": self.booking.booking_reference},
        )

    def test_customer_can_cancel_own_booking_with_reason(self):
        self.client.force_authenticate(self.customer)

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                self.url,
                {"reason": "My travel plans changed."},
                format="json",
            )

        self.booking.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.booking.status, "cancelled")
        self.assertEqual(
            self.booking.cancel_reason,
            "My travel plans changed.",
        )
        self.assertIsNotNone(self.booking.cancelled_at)
        self.assertTrue(
            Notification.objects.filter(
                user=self.admin,
                deduplication_key=(
                    f"customer-cancelled:{self.booking.id}"
                ),
            ).exists()
        )

    def test_customer_cannot_cancel_another_customers_booking(self):
        self.client.force_authenticate(self.other_customer)

        response = self.client.post(
            self.url,
            {"reason": "Not my booking."},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "pending_approval")

    def test_customer_cannot_cancel_after_pickup(self):
        self.booking.status = "picked_up"
        self.booking.save(update_fields=["status"])
        self.client.force_authenticate(self.customer)

        response = self.client.post(
            self.url,
            {"reason": "Cancel after pickup."},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "picked_up")


class AdminBookingLifecycleTests(APITestCase):
    def setUp(self):
        self.admin = Accounts.objects.create_user(
            username="booking-admin@example.com",
            email="booking-admin@example.com",
            password="test-password",
            is_staff=True,
        )
        self.customer = Accounts.objects.create_user(
            username="booking-customer@example.com",
            email="booking-customer@example.com",
            password="test-password",
        )
        car_type = CarType.objects.create(name="Sedan", slug="sedan")
        self.car = Cars.objects.create(
            brand="Toyota",
            model="Vios",
            year=2026,
            car_type=car_type,
            price_per_day=1500,
            transmission="Automatic",
            engine="1.3L",
            fuel_type="Gasoline",
            seats=5,
        )
        self.client.force_authenticate(self.admin)

    def test_admin_cannot_create_booking_at_advanced_status(self):
        response = self.client.post(
            reverse("admin-booking-create"),
            {"status": "completed"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)

    def test_admin_cannot_skip_booking_lifecycle_stages(self):
        pickup_date = timezone.now() + timedelta(days=1)
        booking = Booking.objects.create(
            user=self.customer,
            car=self.car,
            pickup_date=pickup_date,
            return_date=pickup_date + timedelta(days=2),
            pickup_location="Cagayan de Oro",
            return_location="Cagayan de Oro",
            daily_rate=1500,
            number_of_days=2,
            subtotal=3000,
            discount=0,
            total_price=3000,
            status="pending_payment",
        )

        response = self.client.patch(
            reverse(
                "admin-booking-update",
                kwargs={"booking_reference": booking.booking_reference},
            ),
            {"status": "returned"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "pending_payment")

    def test_admin_can_filter_bookings_that_overlap_today(self):
        current_booking = Booking.objects.create(
            user=self.customer,
            car=self.car,
            pickup_date=timezone.now() - timedelta(days=1),
            return_date=timezone.now() + timedelta(days=1),
            daily_rate=1500,
            number_of_days=2,
            subtotal=3000,
            discount=0,
            total_price=3000,
            status="confirmed",
        )
        future_pickup = timezone.now() + timedelta(days=10)
        Booking.objects.create(
            user=self.customer,
            car=self.car,
            pickup_date=future_pickup,
            return_date=future_pickup + timedelta(days=1),
            daily_rate=1500,
            number_of_days=1,
            subtotal=1500,
            discount=0,
            total_price=1500,
            status="confirmed",
        )

        response = self.client.get(
            reverse("admin-bookings"),
            {"rental_period": "today"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["booking_reference"],
            current_booking.booking_reference,
        )


class SimilarCarsTests(APITestCase):
    def setUp(self):
        sedan = CarType.objects.create(name="Similar Sedan", slug="similar-sedan")
        suv = CarType.objects.create(name="Similar SUV", slug="similar-suv")

        self.current_car = Cars.objects.create(
            brand="Toyota",
            model="Vios",
            year=2026,
            car_type=sedan,
            price_per_day=2000,
            transmission="Automatic",
            engine="1.5L",
            fuel_type="Gasoline",
            seats=5,
        )
        self.same_type = Cars.objects.create(
            brand="Honda",
            model="City",
            year=2026,
            car_type=sedan,
            price_per_day=2300,
            transmission="Automatic",
            engine="1.5L",
            fuel_type="Gasoline",
            seats=5,
        )
        self.other_type = Cars.objects.create(
            brand="Ford",
            model="Everest",
            year=2026,
            car_type=suv,
            price_per_day=2050,
            transmission="Automatic",
            engine="2.0L",
            fuel_type="Diesel",
            seats=7,
        )
        Cars.objects.create(
            brand="Unavailable",
            model="Maintenance Car",
            year=2026,
            car_type=sedan,
            price_per_day=2100,
            transmission="Automatic",
            engine="1.5L",
            fuel_type="Gasoline",
            seats=5,
            status="maintenance",
        )

    def test_similar_cars_prioritize_type_and_exclude_current_car(self):
        response = self.client.get(
            reverse(
                "similar-cars",
                kwargs={"car_reference": self.current_car.car_reference},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        references = [item["car_reference"] for item in response.data]
        self.assertEqual(references[0], self.same_type.car_reference)
        self.assertIn(self.other_type.car_reference, references)
        self.assertNotIn(self.current_car.car_reference, references)
        self.assertEqual(len(references), 2)


class AdminAnalyticsTests(APITestCase):
    def setUp(self):
        self.admin = Accounts.objects.create_user(
            username="analytics-admin@example.com",
            email="analytics-admin@example.com",
            password="test-password",
            is_staff=True,
        )
        customer = Accounts.objects.create_user(
            username="analytics-customer@example.com",
            email="analytics-customer@example.com",
            password="test-password",
        )
        car_type = CarType.objects.create(name="Analytics Sedan", slug="analytics-sedan")
        car = Cars.objects.create(
            brand="Toyota",
            model="Altis",
            year=2026,
            car_type=car_type,
            price_per_day=2000,
            transmission="Automatic",
            engine="1.8L",
            fuel_type="Gasoline",
            seats=5,
        )
        pickup_date = timezone.now()
        booking = Booking.objects.create(
            user=customer,
            car=car,
            pickup_date=pickup_date,
            return_date=pickup_date + timedelta(days=1),
            daily_rate=2000,
            number_of_days=1,
            subtotal=2000,
            discount=0,
            total_price=2000,
            status="completed",
        )
        Payment.objects.create(
            booking=booking,
            amount=2000,
            status="paid",
            paid_at=timezone.now(),
        )
        self.client.force_authenticate(self.admin)

    def test_selected_period_drives_stats_and_revenue(self):
        stats_response = self.client.get(
            reverse("admin-analytics-stats"),
            {"period": "30"},
        )
        revenue_response = self.client.get(
            reverse("admin-analytics-revenue"),
            {"period": "30"},
        )
        distribution_response = self.client.get(
            reverse("admin-analytics-status-distribution"),
            {"period": "30"},
        )

        self.assertEqual(stats_response.status_code, status.HTTP_200_OK)
        self.assertEqual(stats_response.data["total_bookings"], 1)
        self.assertEqual(stats_response.data["total_revenue"], 2000.0)
        self.assertEqual(stats_response.data["fleet_utilization"], 3.3)
        self.assertEqual(stats_response.data["cancellation_rate"], 0)

        self.assertEqual(revenue_response.status_code, status.HTTP_200_OK)
        self.assertEqual(revenue_response.data["total"], 2000.0)
        self.assertEqual(
            sum(point["value"] for point in revenue_response.data["points"]),
            2000.0,
        )

        self.assertEqual(distribution_response.status_code, status.HTTP_200_OK)
        self.assertEqual(distribution_response.data["total"], 1)
        completed_status = next(
            item
            for item in distribution_response.data["status_distribution"]
            if item["status"] == "completed"
        )
        self.assertEqual(completed_status["count"], 1)
        self.assertEqual(completed_status["percentage"], 100.0)

    def test_invalid_period_is_rejected(self):
        response = self.client.get(
            reverse("admin-analytics-stats"),
            {"period": "45"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_selected_period_drives_vehicle_and_customer_insights(self):
        vehicles_response = self.client.get(
            reverse("admin-analytics-top-vehicles"),
            {"period": "30"},
        )
        customers_response = self.client.get(
            reverse("admin-analytics-customer-insights"),
            {"period": "30"},
        )

        self.assertEqual(vehicles_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(vehicles_response.data["vehicles"]), 1)
        self.assertEqual(vehicles_response.data["vehicles"][0]["name"], "Toyota Altis")
        self.assertEqual(vehicles_response.data["vehicles"][0]["bookings"], 1)
        self.assertEqual(vehicles_response.data["vehicles"][0]["score"], 100.0)

        self.assertEqual(customers_response.status_code, status.HTTP_200_OK)
        self.assertEqual(customers_response.data["new_customers"], 1)
        self.assertEqual(customers_response.data["returning_customers"], 0)
        self.assertEqual(customers_response.data["average_rental_days"], 1.0)
        self.assertEqual(customers_response.data["average_booking_value"], 2000.0)


class AdminNotificationTests(APITestCase):
    def setUp(self):
        self.admin = Accounts.objects.create_user(
            username="notification-admin@example.com",
            email="notification-admin@example.com",
            password="test-password",
            is_staff=True,
        )
        self.other_admin = Accounts.objects.create_user(
            username="notification-admin-2@example.com",
            email="notification-admin-2@example.com",
            password="test-password",
            is_staff=True,
        )
        self.user = Accounts.objects.create_user(
            username="notification-user@example.com",
            email="notification-user@example.com",
            password="test-password",
        )

    def test_admin_list_only_contains_own_notifications(self):
        own = Notification.objects.create(
            user=self.admin,
            notification_type="system",
            title="Own notification",
            message="Visible",
        )
        Notification.objects.create(
            user=self.other_admin,
            notification_type="system",
            title="Other notification",
            message="Hidden",
        )
        self.client.force_authenticate(self.admin)

        response = self.client.get(reverse("admin-notifications"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], own.id)

    def test_regular_user_cannot_access_admin_notifications(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("admin-notifications"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_mark_all_as_read_and_delete_only_own_notifications(self):
        own_notifications = [
            Notification.objects.create(
                user=self.user,
                notification_type="booking",
                title=f"Own notification {index}",
                message="Visible",
            )
            for index in range(2)
        ]
        other_notification = Notification.objects.create(
            user=self.admin,
            notification_type="system",
            title="Admin notification",
            message="Must remain untouched",
        )
        self.client.force_authenticate(self.user)

        read_response = self.client.patch(
            reverse("notifications-read-all"),
            {},
            format="json",
        )

        self.assertEqual(read_response.status_code, status.HTTP_200_OK)
        self.assertEqual(read_response.data["updated"], 2)
        self.assertFalse(
            Notification.objects.filter(
                id__in=[item.id for item in own_notifications],
                is_read=False,
            ).exists()
        )
        other_notification.refresh_from_db()
        self.assertFalse(other_notification.is_read)

        delete_response = self.client.delete(
            reverse("notifications-delete-all"),
        )

        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertFalse(Notification.objects.filter(user=self.user).exists())
        self.assertTrue(Notification.objects.filter(pk=other_notification.pk).exists())

    def test_admin_notification_creation_is_deduplicated_per_recipient(self):
        payload = {
            "notification_type": "payment",
            "title": "Payment received",
            "message": "A payment was received.",
            "deduplication_key": "payment-paid:1",
        }

        create_admin_notifications(**payload)
        create_admin_notifications(**payload)

        self.assertEqual(
            Notification.objects.filter(
                deduplication_key="payment-paid:1"
            ).count(),
            2,
        )

    def test_admin_can_mark_all_as_read_and_delete_own_notification(self):
        notification = Notification.objects.create(
            user=self.admin,
            notification_type="booking",
            title="New booking",
            message="A booking was created.",
        )
        self.client.force_authenticate(self.admin)

        read_response = self.client.patch(
            reverse("admin-notifications-read-all"),
            {},
            format="json",
        )
        notification.refresh_from_db()

        self.assertEqual(read_response.status_code, status.HTTP_200_OK)
        self.assertTrue(notification.is_read)

        delete_response = self.client.delete(
            reverse(
                "admin-notification-delete",
                kwargs={"notification_id": notification.id},
            )
        )
        self.assertEqual(
            delete_response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Notification.objects.filter(pk=notification.id).exists()
        )

    def test_unread_count_generates_maintenance_and_overdue_reminders(self):
        car_type = CarType.objects.create(name="SUV", slug="suv")
        car = Cars.objects.create(
            brand="Ford",
            model="Everest",
            year=2026,
            car_type=car_type,
            price_per_day=3000,
            transmission="Automatic",
            engine="2.0L",
            fuel_type="Diesel",
            seats=7,
            status="maintenance",
        )
        Booking.objects.create(
            user=self.user,
            car=car,
            pickup_date=timezone.now() - timedelta(days=3),
            return_date=timezone.now() - timedelta(days=1),
            pickup_location="Cagayan de Oro",
            return_location="Cagayan de Oro",
            daily_rate=3000,
            number_of_days=2,
            subtotal=6000,
            discount=0,
            total_price=6000,
            status="picked_up",
        )
        self.client.force_authenticate(self.admin)

        first = self.client.get(reverse("admin-notification-unread-count"))
        second = self.client.get(reverse("admin-notification-unread-count"))

        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(first.data["unread_count"], 2)
        self.assertEqual(second.data["unread_count"], 2)

    def test_backfill_command_creates_historical_notifications_once(self):
        car_type = CarType.objects.create(name="Van", slug="van")
        Cars.objects.create(
            brand="Toyota",
            model="Hiace",
            year=2026,
            car_type=car_type,
            price_per_day=3500,
            transmission="Manual",
            engine="2.8L",
            fuel_type="Diesel",
            seats=12,
            status="maintenance",
        )
        output = StringIO()
        call_command("backfill_admin_notifications", stdout=output)
        call_command("backfill_admin_notifications", stdout=output)

        self.assertIn("processed", output.getvalue())
        self.assertEqual(
            Notification.objects.filter(
                deduplication_key__startswith="historical-"
            ).count(),
            2,
        )

    def test_failed_payment_webhook_notifies_admins(self):
        car_type = CarType.objects.create(name="Pickup", slug="pickup")
        car = Cars.objects.create(
            brand="Ford",
            model="Ranger",
            year=2026,
            car_type=car_type,
            price_per_day=2500,
            transmission="Automatic",
            engine="2.0L",
            fuel_type="Diesel",
            seats=5,
        )
        booking = Booking.objects.create(
            user=self.user,
            car=car,
            pickup_date=timezone.now() + timedelta(days=1),
            return_date=timezone.now() + timedelta(days=2),
            daily_rate=2500,
            number_of_days=1,
            subtotal=2500,
            discount=0,
            total_price=2500,
        )
        payment = Payment.objects.create(
            booking=booking,
            amount=2500,
            status="pending",
        )

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("paymongo-webhook"),
                {
                    "data": {
                        "id": "evt_failed_payment_test",
                        "attributes": {
                            "type": "payment.failed",
                            "data": {
                                "attributes": {
                                    "metadata": {
                                        "booking_id": str(booking.id),
                                    }
                                }
                            }
                        },
                    }
                },
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment.refresh_from_db()
        booking.refresh_from_db()
        self.assertEqual(payment.status, "failed")
        self.assertEqual(booking.status, "payment_failed")
        self.assertEqual(
            Notification.objects.filter(
                deduplication_key="payment-failed:evt_failed_payment_test"
            ).count(),
            2,
        )

    def test_checkout_v2_paid_webhook_marks_payment_as_paid(self):
        car_type = CarType.objects.create(name="Sedan", slug="webhook-sedan")
        car = Cars.objects.create(
            brand="Toyota",
            model="Vios",
            year=2026,
            car_type=car_type,
            price_per_day=2000,
            transmission="Automatic",
            engine="1.5L",
            fuel_type="Gasoline",
            seats=5,
        )
        booking = Booking.objects.create(
            user=self.user,
            car=car,
            pickup_date=timezone.now() + timedelta(days=1),
            return_date=timezone.now() + timedelta(days=2),
            daily_rate=2000,
            number_of_days=1,
            subtotal=2000,
            discount=0,
            total_price=2000,
        )
        payment = Payment.objects.create(
            booking=booking,
            checkout_session_id="cs_checkout_v2_test",
            amount=2000,
            status="pending",
        )

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("paymongo-webhook"),
                {
                    "event_type": "send.webhook",
                    "data": {
                        "type": "checkout_session.payment.paid",
                        "data": {
                            "id": "cs_checkout_v2_test",
                            "attributes": {
                                "payment_intent": {"id": "pi_checkout_v2_test"},
                                "payments": [
                                    {
                                        "id": "pay_checkout_v2_test",
                                        "attributes": {
                                            "status": "paid",
                                            "source": {"type": "card"},
                                        },
                                    }
                                ],
                            },
                        },
                    },
                },
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment.refresh_from_db()
        booking.refresh_from_db()
        self.assertEqual(payment.status, "paid")
        self.assertIsNotNone(payment.paid_at)
        self.assertEqual(payment.payment_intent_id, "pi_checkout_v2_test")
        self.assertEqual(payment.paymongo_payment_id, "pay_checkout_v2_test")
        self.assertEqual(payment.payment_method, "card")
        self.assertEqual(booking.status, "pending_approval")
        self.assertEqual(
            Notification.objects.filter(
                user=self.user,
                booking=booking,
                title="Booking Created",
            ).count(),
            1,
        )
        self.assertEqual(
            Notification.objects.filter(
                deduplication_key=f"payment-paid:{payment.id}"
            ).count(),
            2,
        )


class RefundFlowTests(APITestCase):
    def setUp(self):
        self.customer = Accounts.objects.create_user(
            username="refund-customer@example.com",
            email="refund-customer@example.com",
            password="test-password",
        )
        self.admin = Accounts.objects.create_user(
            username="refund-admin@example.com",
            email="refund-admin@example.com",
            password="test-password",
            is_staff=True,
        )
        car_type = CarType.objects.create(name="Refund Sedan", slug="refund-sedan")
        self.car = Cars.objects.create(
            brand="Toyota",
            model="Vios",
            year=2026,
            car_type=car_type,
            price_per_day=2000,
            transmission="Automatic",
            engine="1.5L",
            fuel_type="Gasoline",
            seats=5,
        )

    def create_paid_booking(self, status_value="pending_approval"):
        booking = Booking.objects.create(
            user=self.customer,
            car=self.car,
            pickup_date=timezone.now() + timedelta(days=2),
            return_date=timezone.now() + timedelta(days=3),
            pickup_location="Cagayan de Oro",
            return_location="Cagayan de Oro",
            daily_rate=2000,
            number_of_days=1,
            subtotal=2000,
            discount=0,
            total_price=2000,
            status=status_value,
        )
        payment = Payment.objects.create(
            booking=booking,
            paymongo_payment_id=f"pay_{booking.id}",
            amount=2000,
            status="paid",
            paid_at=timezone.now(),
        )
        return booking, payment

    def test_paid_customer_cancellation_creates_refund_review(self):
        booking, payment = self.create_paid_booking()
        self.client.force_authenticate(self.customer)

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse(
                    "booking-cancel",
                    kwargs={"booking_reference": booking.booking_reference},
                ),
                {"reason": "My travel plans changed."},
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refund = Refund.objects.get(payment=payment)
        self.assertEqual(refund.status, "pending_review")
        self.assertEqual(refund.amount, payment.amount)
        self.assertEqual(refund.requested_by, self.customer)
        self.assertEqual(response.data["refund"]["status"], "pending_review")

    @patch("driveease.views.payments.requests.post")
    def test_admin_can_issue_full_refund(self, mocked_post):
        booking, payment = self.create_paid_booking(status_value="cancelled")
        Refund.objects.create(
            payment=payment,
            amount=payment.amount,
            requested_by=self.customer,
            customer_reason="Plans changed.",
        )
        mocked_post.return_value.ok = True
        mocked_post.return_value.json.return_value = {
            "data": {
                "id": "ref_test_success",
                "type": "refund",
                "attributes": {
                    "amount": 200000,
                    "payment_id": payment.paymongo_payment_id,
                    "status": "succeeded",
                },
            }
        }
        self.client.force_authenticate(self.admin)

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse(
                    "admin-booking-refund",
                    kwargs={"booking_reference": booking.booking_reference},
                ),
                {"note": "Approved customer cancellation."},
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment.refresh_from_db()
        refund = payment.refunds.get()
        self.assertEqual(payment.status, "refunded")
        self.assertEqual(refund.status, "succeeded")
        self.assertEqual(refund.paymongo_refund_id, "ref_test_success")
        self.assertEqual(refund.reviewed_by, self.admin)
        self.assertTrue(
            AdminActivityLog.objects.filter(
                admin=self.admin,
                target_type="refund",
            ).exists()
        )
        mocked_post.assert_called_once()

    def test_customer_cannot_issue_refund(self):
        booking, _ = self.create_paid_booking(status_value="cancelled")
        self.client.force_authenticate(self.customer)

        response = self.client.post(
            reverse(
                "admin-booking-refund",
                kwargs={"booking_reference": booking.booking_reference},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_refund_webhook_marks_full_payment_refunded(self):
        booking, payment = self.create_paid_booking(status_value="cancelled")
        refund = Refund.objects.create(
            payment=payment,
            paymongo_refund_id="ref_webhook_test",
            amount=payment.amount,
            status="processing",
            reviewed_by=self.admin,
        )

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("paymongo-webhook"),
                {
                    "data": {
                        "id": "evt_refund_success",
                        "attributes": {
                            "type": "payment.refund.updated",
                            "data": {
                                "id": refund.paymongo_refund_id,
                                "type": "refund",
                                "attributes": {
                                    "amount": 200000,
                                    "payment_id": payment.paymongo_payment_id,
                                    "status": "succeeded",
                                },
                            },
                        },
                    }
                },
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment.refresh_from_db()
        refund.refresh_from_db()
        self.assertEqual(payment.status, "refunded")
        self.assertEqual(refund.status, "succeeded")
        self.assertIsNotNone(refund.processed_at)

class LogoutTests(APITestCase):
    def setUp(self):
        self.user = Accounts.objects.create_user(
            username="logout@example.com",
            email="logout@example.com",
            password="test-password",
        )
        self.url = reverse("auth-logout")

    def test_logout_blacklists_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies[settings.JWT_REFRESH_COOKIE_NAME] = str(refresh)

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(
            BlacklistedToken.objects.filter(token__jti=refresh["jti"]).exists()
        )

    def test_logout_is_safe_without_a_valid_token(self):
        self.client.cookies[settings.JWT_REFRESH_COOKIE_NAME] = "not-a-token"
        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RefreshCookieTests(APITestCase):
    def setUp(self):
        self.user = Accounts.objects.create_user(
            username="refresh@example.com",
            email="refresh@example.com",
            password="test-password",
        )
        self.url = reverse("token-refresh")

    def test_refresh_uses_httponly_cookie_and_rotates_it(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies[settings.JWT_REFRESH_COOKIE_NAME] = str(refresh)

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertNotIn("refresh", response.data)

        cookie = response.cookies[settings.JWT_REFRESH_COOKIE_NAME]
        self.assertTrue(cookie["httponly"])
        self.assertEqual(cookie["path"], settings.JWT_REFRESH_COOKIE_PATH)
        self.assertNotEqual(cookie.value, str(refresh))

    def test_blacklisted_refresh_token_returns_unauthorized(self):
        refresh = RefreshToken.for_user(self.user)
        refresh.blacklist()
        self.client.cookies[settings.JWT_REFRESH_COOKIE_NAME] = str(refresh)

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Refresh token is invalid or expired",
        )

    def test_refresh_token_in_request_body_is_rejected(self):
        refresh = RefreshToken.for_user(self.user)

        response = self.client.post(
            self.url,
            {"refresh": str(refresh)},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_rejects_unapproved_browser_origin(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies[settings.JWT_REFRESH_COOKIE_NAME] = str(refresh)

        response = self.client.post(
            self.url,
            {},
            format="json",
            HTTP_ORIGIN="https://attacker.example",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
