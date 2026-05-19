from django.contrib import admin

from .models import Booking, AvailableSlot, User

# Register your models here.
admin.site.register(Booking)
admin.site.register(AvailableSlot)
admin.site.register(User)
