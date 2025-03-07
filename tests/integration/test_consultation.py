import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.infrastructure.db.models import Consultation, Doctor, Patient, Profile

User = get_user_model()


@pytest.fixture
def setup_data():
    # Создаем тестовые данные
    doctor = Doctor.objects.create(
        first_name='Иван',
        last_name='Иванов',
        middle_name='Иванович',
        specialization='Терапевт'
    )
    patient = Patient.objects.create(
        first_name='Петр',
        last_name='Петров',
        middle_name='Петрович',
        phone='+79991234567',
        email='petr@example.com'
    )
    consultation1 = Consultation.objects.create(
        doctor=doctor,
        patient=patient,
        created_at='2025-03-05T10:00:00Z',
        started_at='2025-03-05T10:00:00Z',
        status='pending'
    )
    consultation2 = Consultation.objects.create(
        doctor=doctor,
        patient=patient,
        created_at='2025-03-05T11:00:00Z',
        started_at='2025-03-05T11:00:00Z',
        status='confirmed'
    )
    consultation3 = Consultation.objects.create(
        doctor=doctor,
        patient=patient,
        created_at='2025-03-05T12:00:00Z',
        started_at='2025-03-05T12:00:00Z',
        status='completed'
    )
    return consultation1, consultation2, consultation3


@pytest.mark.django_db
def test_filter_by_status(setup_data):
    consultation1, consultation2, consultation3 = setup_data

    # Логинимся
    client = APIClient()
    user = User.objects.create_user(username='admin', password='admin123')
    Profile.objects.create(user=user, role='admin')
    token_response = client.post(
        '/api/v1/auth',
        {'username': 'admin', 'password': 'admin123'},
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_response.data["access"]}')

    # Фильтрация по статусу 'confirmed'
    response = client.get('/api/v1/consultations?status=confirmed')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['status'] == 'confirmed'


@pytest.mark.django_db
def test_search_by_doctor_name(setup_data):
    consultation1, consultation2, consultation3 = setup_data

    # Логинимся
    client = APIClient()
    user = User.objects.create_user(username='admin', password='admin123')
    Profile.objects.create(user=user, role='admin')
    token_response = client.post(
        '/api/v1/auth',
        {'username': 'admin', 'password': 'admin123'},
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_response.data["access"]}')

    # Поиск по имени врача 'Иван'
    response = client.get('/api/v1/consultations?doctor_name=Иван')
    assert response.status_code == 200
    assert len(response.data) == 3


@pytest.mark.django_db
def test_search_by_patient_name(setup_data):
    consultation1, consultation2, consultation3 = setup_data

    # Логинимся
    client = APIClient()
    user = User.objects.create_user(username='admin', password='admin123')
    Profile.objects.create(user=user, role='admin')
    token_response = client.post(
        '/api/v1/auth',
        {'username': 'admin', 'password': 'admin123'},
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_response.data["access"]}')

    # Поиск по имени пациента 'Петр'
    response = client.get('/api/v1/consultations?patient_name=Петр')
    assert response.status_code == 200
    assert len(response.data) == 3


@pytest.mark.django_db
def test_sort_by_date(setup_data):
    consultation1, consultation2, consultation3 = setup_data

    # Логинимся
    client = APIClient()
    user = User.objects.create_user(username='admin', password='admin123')
    Profile.objects.create(user=user, role='admin')
    token_response = client.post(
        '/api/v1/auth',
        {'username': 'admin', 'password': 'admin123'},
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_response.data["access"]}')

    # Сортировка по дате консультации
    response = client.get('/api/v1/consultations?sort_asc=desc')
    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[0]['created_at'] == '2025-03-05T12:00:00Z'
    assert response.data[1]['created_at'] == '2025-03-05T11:00:00Z'
    assert response.data[2]['created_at'] == '2025-03-05T10:00:00Z'


@pytest.mark.django_db
def test_update_consultation_status_valid(setup_data):
    consultation1, consultation2, consultation3 = setup_data

    # Логинимся
    client = APIClient()
    user = User.objects.create_user(username='admin', password='admin123')
    Profile.objects.create(user=user, role='admin')
    token_response = client.post(
        '/api/v1/auth',
        {'username': 'admin', 'password': 'admin123'},
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_response.data["access"]}')

    # Обновляем статус на 'confirmed'
    response = client.patch(
        f'/api/v1/consultations/{consultation1.id}/status',
        {'status': 'confirmed'},
        format='json'
    )

    assert response.status_code == 200
    assert response.data['status'] == 'confirmed'


@pytest.mark.django_db
def test_update_consultation_status_invalid(setup_data):
    consultation1, consultation2, consultation3 = setup_data

    # Логинимся
    client = APIClient()
    user = User.objects.create_user(username='admin', password='admin123')
    Profile.objects.create(user=user, role='admin')
    token_response = client.post(
        '/api/v1/auth',
        {'username': 'admin', 'password': 'admin123'},
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_response.data["access"]}')

    # Пытаемся обновить статус на недопустимый статус
    response = client.patch(
        f'/api/v1/consultations/{consultation1.id}/status',
        {'status': 'invalid_status'},
        format='json'
    )

    assert response.status_code == 400
    assert 'Недопустимый статус' in response.data['detail']


@pytest.mark.django_db
def test_update_consultation_status_not_found(setup_data):
    consultation1, consultation2, consultation3 = setup_data

    # Логинимся
    client = APIClient()
    user = User.objects.create_user(username='admin', password='admin123')
    Profile.objects.create(user=user, role='admin')
    token_response = client.post(
        '/api/v1/auth',
        {'username': 'admin', 'password': 'admin123'},
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_response.data["access"]}')

    # Пытаемся обновить статус несуществующей консультации
    response = client.patch(
        '/api/v1/consultations/999/status',
        {'status': 'confirmed'},
        format='json'
    )

    assert response.status_code == 404
    assert 'Консультация не найдена' in response.data['detail']


@pytest.mark.django_db
def test_update_consultation_status_missing_status(setup_data):
    consultation1, consultation2, consultation3 = setup_data

    # Логинимся
    client = APIClient()
    user = User.objects.create_user(username='admin', password='admin123')
    Profile.objects.create(user=user, role='admin')
    token_response = client.post(
        '/api/v1/auth',
        {'username': 'admin', 'password': 'admin123'},
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_response.data["access"]}')

    # Пытаемся обновить статус без указания нового статуса
    response = client.patch(
        f'/api/v1/consultations/{consultation1.id}/status',
        {},
        format='json'
    )

    assert response.status_code == 400
    assert 'Недопустимый статус' in response.data['detail']
