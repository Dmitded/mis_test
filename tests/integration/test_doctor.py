import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.infrastructure.db.models import Doctor, Clinic, Profile

User = get_user_model()


@pytest.mark.django_db
def test_add_doctor_to_clinic_as_admin():
    # Создаем пользователя-админа
    user = User.objects.create_user(username='admin', password='admin123')
    Profile.objects.create(user=user, role='admin')

    # Создаем доктора и клинику
    doctor = Doctor.objects.create(first_name='Иван', last_name='Иванов', middle_name='Иванович', specialization='Терапевт')
    clinic = Clinic.objects.create(name='Клиника №1', legal_address='ул. Ленина, 1', physical_address='ул. Ленина, 1')

    # Логинимся
    client = APIClient()
    token_response = client.post(
        '/api/v1/auth',
        {'username': 'admin', 'password': 'admin123'},
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_response.data["access"]}')

    # Добавляем доктора в клинику
    response = client.post(
        f'/api/v1/doctors/{doctor.id}/add_clinic',
        {'clinic_id': clinic.id},
        format='json'
    )

    assert response.status_code == 200
    assert doctor.clinics.filter(id=clinic.id).exists()


@pytest.mark.django_db
def test_add_doctor_to_clinic_as_doctor():
    # Создаем доктора, пользователя и профиль
    doctor = Doctor.objects.create(first_name='Иван', last_name='Иванов', middle_name='Иванович', specialization='Терапевт')
    user = User.objects.create_user(username='doctor', password='doctor123')
    Profile.objects.create(user=user, role='doctor', doctor=doctor)

    # Создаем клинику
    clinic = Clinic.objects.create(name='Клиника №1', legal_address='ул. Ленина, 1', physical_address='ул. Ленина, 1')

    # Логинимся
    client = APIClient()
    token_response = client.post(
        '/api/v1/auth',
        {'username': 'doctor', 'password': 'doctor123'},
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_response.data["access"]}')

    # Пытаемся добавить доктора в клинику
    response = client.post(
        f'/api/v1/doctors/{doctor.id}/add_clinic',
        {'clinic_id': clinic.id},
        format='json'
    )

    assert response.status_code == 403  # Доступ запрещен
