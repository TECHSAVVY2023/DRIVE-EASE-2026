from django.contrib import admin
from .models import Cars, CarImage, ContactListModel, UserProfile


admin.site.register(ContactListModel)
admin.site.register(UserProfile)


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]