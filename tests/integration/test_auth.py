import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.infrastructure.db.models import Doctor, Patient, Profile

User = get_user_model()


@pytest.mark.django_db
def test_login_as_admin():
    # Создаем пользователя и профиль с ролью админа
    user = User.objects.create_user(username='admin', password='admin123')
    Profile.objects.create(user=user, role='admin')

    # Логинимся
    client = APIClient()
    response = client.post(
        '/api/v1/auth',
        {'username': 'admin', 'password': 'admin123'},
        format='json'
    )

    assert response.status_code == 200
    assert response.data['role'] == 'admin'
    assert response.data['doctor_id'] is None
    assert response.data['patient_id'] is None


@pytest.mark.django_db
def test_login_as_doctor():
    # Создаем доктора, пользователя и профиль
    doctor = Doctor.objects.create(first_name='Иван', last_name='Иванов', middle_name='Иванович', specialization='Терапевт')
    user = User.objects.create_user(username='doctor', password='doctor123')
    Profile.objects.create(user=user, role='doctor', doctor=doctor)

    # Логинимся
    client = APIClient()
    response = client.post(
        '/api/v1/auth',
        {'username': 'doctor', 'password': 'doctor123'},
        format='json'
    )

    assert response.status_code == 200
    assert response.data['role'] == 'doctor'
    assert response.data['doctor_id'] == doctor.id
    assert response.data['patient_id'] is None


@pytest.mark.django_db
def test_login_as_patient():
    # Создаем пациента, пользователя и профиль
    patient = Patient.objects.create(first_name='Петр', last_name='Петров', middle_name='Петрович', phone='+79991234567', email='petr@example.com')
    user = User.objects.create_user(username='patient', password='patient123')
    Profile.objects.create(user=user, role='patient', patient=patient)

    # Логинимся
    client = APIClient()
    response = client.post(
        '/api/v1/auth',
        {'username': 'patient', 'password': 'patient123'},
        format='json'
    )

    assert response.status_code == 200
    assert response.data['role'] == 'patient'
    assert response.data['patient_id'] == patient.id
    assert response.data['doctor_id'] is None


@pytest.mark.django_db
def test_refresh_token():
    # Создаем пользователя и профиль
    user = User.objects.create_user(username='admin', password='admin123')
    Profile.objects.create(user=user, role='admin')

    # Логинимся
    client = APIClient()
    login_response = client.post(
        '/api/v1/auth',
        {'username': 'admin', 'password': 'admin123'},
        format='json'
    )

    # Обновляем access токен
    refresh_response = client.post(
        '/api/v1/auth/refresh',
        {'refresh': login_response.data['refresh']},
        format='json'
    )

    assert refresh_response.status_code == 200
    assert 'access' in refresh_response.data


@pytest.mark.django_db
def test_login_failure():
    # Логинимся с неверными данными
    client = APIClient()
    response = client.post(
        '/api/v1/auth',
        {'username': 'wronguser', 'password': 'wrongpassword'},
        format='json'
    )

    assert response.status_code == 401
    assert response.data['detail'] == 'Invalid credentials'
