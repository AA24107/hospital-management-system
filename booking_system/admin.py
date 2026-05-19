from django.contrib import admin

from .models import Booking, AvailableSlot, User, GoogleCredentials

# Register your models here.
admin.site.register(Booking)
admin.site.register(AvailableSlot)
admin.site.register(User)
admin.site.register(GoogleCredentials)
