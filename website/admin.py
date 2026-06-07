from django.contrib import admin
from .models import Trip, TripSchedule, Booking

# Register your models here.
admin.site.register(Trip)
admin.site.register(TripSchedule)
admin.site.register(Booking)