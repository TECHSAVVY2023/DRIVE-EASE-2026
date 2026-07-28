from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cars, Accounts, FileUploadModel, ContactListModel, Reviews, ReviewHelpful, Booking, Payment

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

admin.site.register(ReviewHelpful)
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
        "location",
        "total_price",
        "status",
        "created_at",
    )
    list_filter = ("status", "pickup_date", "created_at")
    search_fields = ("booking_reference", "user__email", "car__car_id", "location")
    readonly_fields = ("booking_reference", "created_at", "updated_at")

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