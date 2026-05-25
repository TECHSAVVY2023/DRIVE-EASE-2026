from django.contrib import admin
from .models import Cars, ContactListModel

# Register your models here.
admin.site.register(ContactListModel)
admin.site.register(Cars)