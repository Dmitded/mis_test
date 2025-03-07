from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.infrastructure.db.models import (
    Profile, Doctor, Patient, Clinic, DoctorClinic, Consultation
)
from datetime import datetime, timedelta
import random
import pytz


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write("Создание тестовых данных...")

        # Очистка старых данных
        self.stdout.write("Очистка старых данных...")
        Consultation.objects.all().delete()
        DoctorClinic.objects.all().delete()
        Clinic.objects.all().delete()
        Doctor.objects.all().delete()
        Patient.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

        # Создание пользователей и профилей
        self.stdout.write("Создание пользователей и профилей...")
        roles = ['admin', 'doctor', 'patient']
        for i in range(1, 6):
            user = User.objects.create_user(
                username=f'user{i}',
                password=f'password{i}',
                email=f'user{i}@example.com'
            )
            role = random.choice(roles)
            profile = Profile.objects.create(
                user=user,
                role=role
            )
            if role == 'doctor':
                doctor = Doctor.objects.create(
                    first_name=f'Doctor{i}',
                    last_name=f'Lastname{i}',
                    middle_name=f'Middlename{i}',
                    specialization=f'Specialization{i}'
                )
                profile.doctor = doctor
                profile.save()
            elif role == 'patient':
                patient = Patient.objects.create(
                    first_name=f'Patient{i}',
                    last_name=f'Lastname{i}',
                    middle_name=f'Middlename{i}',
                    phone=f'+7999123456{i}',
                    email=f'patient{i}@example.com'
                )
                profile.patient = patient
                profile.save()

        # Создание клиник
        self.stdout.write("Создание клиник...")
        clinics = []
        for i in range(1, 4):
            clinic = Clinic.objects.create(
                name=f'Clinic {i}',
                legal_address=f'Legal Address {i}',
                physical_address=f'Physical Address {i}'
            )
            clinics.append(clinic)

        # Создание связей DoctorClinic
        self.stdout.write("Создание связей DoctorClinic...")
        doctors = Doctor.objects.all()
        for doctor in doctors:
            clinic = random.choice(clinics)
            DoctorClinic.objects.create(
                doctor=doctor,
                clinic=clinic
            )

        # Создание консультаций
        self.stdout.write("Создание консультаций...")
        patients = Patient.objects.all()
        statuses = ['pending', 'confirmed', 'started', 'completed', 'paid']
        for i in range(1, 11):
            doctor = random.choice(doctors)
            patient = random.choice(patients)
            created_at = datetime.now(tz=pytz.UTC)
            Consultation.objects.create(
                doctor=doctor,
                patient=patient,
                created_at=created_at,
                started_at=created_at + timedelta(days=random.randint(1, 30)),
                status=random.choice(statuses)
            )

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы!"))
