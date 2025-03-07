from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('doctor', 'doctor'),
        ('patient', 'patient'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    doctor = models.OneToOneField('Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')
    patient = models.OneToOneField('Patient', on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')

    class Meta:
        db_table = 'profile'


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    # relations
    clinics = models.ManyToManyField("Clinic", through='DoctorClinic', blank=True)

    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return f'id({self.id}) {self.first_name} {self.middle_name}'


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    class Meta:
        db_table = 'patient'

    def __str__(self):
        return f'id({self.id}) {self.first_name} {self.middle_name}'


class Clinic(models.Model):
    name = models.CharField(max_length=100)
    legal_address = models.CharField(max_length=200)
    physical_address = models.CharField(max_length=200)

    class Meta:
        db_table = 'clinic'

    def __str__(self):
        return f'id({self.id}) {self.name}'

class DoctorClinic(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    class Meta:
        db_table = 'doctor_clinic'


class Consultation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждена'),
        ('started', 'Начата'),
        ('completed', 'Завершена'),
        ('paid', 'Оплачена'),
    ]
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    started_at = models.DateTimeField(null=False)
    finished_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = 'consultation'
