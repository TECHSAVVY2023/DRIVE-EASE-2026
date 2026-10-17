from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cars, Accounts, FileUploadModel, ContactListModel, Reviews, ReviewHelpful, Booking, Payment, Feature, Notification, CarType
from .tasks import create_notification

admin.site.register(Cars)

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "car",
        "user",
        "rating",
        "text",
        "created_at",
    )


admin.site.register(Feature)
admin.site.register(ReviewHelpful)
admin.site.register(CarType)
admin.site.register(ContactListModel)

@admin.register(Accounts)
class AccountsAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Profile",
            {
                "fields": (
                    "profile_picture",
                    "id_images",
                )
            },
        ),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_reference",
        "user",
        "car",
        "pickup_date",
        "return_date",
        "pickup_location",
        "return_location",
        "total_price",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "pickup_date",
        "created_at",
    )

    search_fields = (
        "booking_reference",
        "user__email",
        "car__car_id",
        "pickup_location",
        "return_location",
    )

    readonly_fields = (
        "booking_reference",
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        """
        Detect booking status changes when an admin saves a booking.
        If the status changes, create a notification through Celery.
        """

        old_status = None

        # Get the previous status before saving
        if change:
            old_booking = Booking.objects.get(pk=obj.pk)
            old_status = old_booking.status

        # Save the booking normally
        super().save_model(request, obj, form, change)

        # Only send a notification when the status actually changed
        if not change or old_status == obj.status:
            return

        # Notifications for each relevant booking status
        notifications = {
            "confirmed": {
                "title": "Booking Confirmed",
                "message": (
                    f"Your booking {obj.booking_reference} "
                    "has been confirmed."
                ),
            },

            "rejected": {
                "title": "Booking Rejected",
                "message": (
                    f"Your booking {obj.booking_reference} "
                    "has been rejected."
                ),
            },

            "picked_up": {
                "title": "Vehicle Picked Up",
                "message": (
                    f"Your booking {obj.booking_reference} "
                    "has been marked as picked up."
                ),
            },

            "returned": {
                "title": "Vehicle Returned",
                "message": (
                    f"Your booking {obj.booking_reference} "
                    "has been marked as returned."
                ),
            },

            "completed": {
                "title": "Booking Completed",
                "message": (
                    f"Your booking {obj.booking_reference} "
                    "has been completed."
                ),
            },

            "cancelled": {
                "title": "Booking Cancelled",
                "message": (
                    f"Your booking {obj.booking_reference} "
                    "has been cancelled."
                ),
            },
        }

        notification = notifications.get(obj.status)

        # Only create a notification for statuses we defined above
        if notification:
            create_notification.delay(
                user_id=obj.user_id,
                notification_type="booking_status",
                title=notification["title"],
                message=notification["message"],
                booking_id=obj.id,
            )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_intent_id",
        "checkout_session_id",
        "booking",
        "amount",
        "currency",
        "status",
        "paid_at",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("payment_intent_id", "checkout_session_id", "booking__booking_reference")
    readonly_fields = ("payment_intent_id", "checkout_session_id", "created_at", "updated_at", "paymongo_response")

@admin.register(FileUploadModel)
class FileUploadModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file",
        "uploaded_at",
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "notification_type",
        "title",
        "message",
        "is_read",
        "created_at",
    )
    list_filter = ("is_read", "created_at")
    search_fields = ("title", "message")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"