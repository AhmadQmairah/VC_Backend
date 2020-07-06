from django.contrib import admin
from .models import Patient, Appointment, AppointmentBooking, MedHistory
# Register your models here.
admin.site.register([Patient, Appointment, AppointmentBooking, MedHistory])
