from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=[('doctor', 'Doctor'), ('patient', 'Patient')])
   

class Booking(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_as_doctor')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_as_patient')
    slot = models.OneToOneField('AvailableSlot', on_delete=models.CASCADE, related_name='booking')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.patient.role != 'patient':
            raise ValidationError("Booking user must be a patient")

        if self.doctor.role != 'doctor':
            raise ValidationError("Doctor must have doctor role")

        if self.slot.doctor != self.doctor:
            raise ValidationError("Slot does not belong to this doctor")

        if self.slot.is_booked:
            raise ValidationError("Slot already booked")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.slot.is_booked = True
        self.slot.save()

    def __str__(self):
        return f"{self.patient.username} booked {self.slot.start_time} by {self.doctor.username}"


class AvailableSlot(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='available_slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.doctor.role != 'doctor':
            raise ValueError("Only doctors can create slots")
        super().save(*args, **kwargs)

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time")

        if not self.pk and self.start_time < timezone.now():
            raise ValidationError("Slot cannot be in the past")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'start_time', 'end_time'],
                name='unique_doctor_slot'
            )
        ]

    def __str__(self):
        return f"{self.doctor.username} | {self.start_time}"


class GoogleCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    access_token = models.TextField()
    refresh_token = models.TextField()

    token_uri = models.URLField(default='https://oauth2.googleapis.com/token')

    client_id = models.TextField()
    client_secret = models.TextField()

    scopes = models.TextField()