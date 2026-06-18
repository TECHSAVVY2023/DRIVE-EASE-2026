from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Cars, ContactListModel, Profile, FileUploadModel

User = get_user_model()

admin.site.register(Cars)
admin.site.register(ContactListModel)

@admin.register(Profile) 
class ProfileAdmin(admin.ModelAdmin): 
    list_display = (
        "id",
        "user",
        "contact_number",
        "address",
        "profile_picture",
        "id_images",
    )

admin.site.unregister(User)

@admin.register(User) 
class CustomUserAdmin(UserAdmin): 
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )

admin.site.register(FileUploadModel)
class FileUploadModel(admin.ModelAdmin):
    list_display = (
        "id",
        "file",
        "uploaded_at",
    )