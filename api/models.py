from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Patient(models.Model):
    YEAR_IN_SCHOOL_CHOICES = [
        ("Approved", 'Approved'),
        ("Rejected", 'Rejected'),
        ("Not Checked", 'Not Checked'),

    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    civil_id = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    is_doctor = models.BooleanField(default=False, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    doctor_image = models.ImageField(upload_to='images', null=True, blank=True)
    dcctor_speciality = models.CharField(max_length=30, null=True, blank=True)
    doctor_verified = models.CharField(
        max_length=30, choices=YEAR_IN_SCHOOL_CHOICES, default="Not Checked", null=True, blank=True)


class AppointmentBooking(models.Model):
    YEAR_IN_SCHOOL_CHOICES = [
        ("Approved", 'Approved'),
        ("Rejected", 'Rejected'),
        ("Pending", 'Pending'),
        ("Cancelled", 'Cancelled'),

    ]
    image = models.ImageField(upload_to='images', null=True, blank=True)
    description = models.CharField(max_length=30, null=True, blank=True)
    user = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=30, choices=YEAR_IN_SCHOOL_CHOICES, default="Pending", null=True, blank=True)


class Appointment(models.Model):
    time = models.TimeField()
    end_time = models.TimeField(null=True)
    date = models.DateField()
    doctor = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True)
    booked_by = models.OneToOneField(
        AppointmentBooking, on_delete=models.CASCADE, null=True, blank=True)


class MedHistory(models.Model):
    user = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True, related_name="history")
    description = models.CharField(max_length=30, null=True, blank=True)
