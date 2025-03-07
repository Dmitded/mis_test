import pytest
from django.contrib.auth.models import User
from apps.domain.services.auth_service import AuthService
from apps.infrastructure.db.models import Profile


@pytest.mark.django_db
def test_authenticate_success():
    # Создаем пользователя и профиль
    user = User.objects.create_user(username='testuser', password='testpassword')
    Profile.objects.create(user=user, role='admin')

    # Тестируем аутентификацию
    auth_service = AuthService()
    authenticated_user = auth_service.authenticate('testuser', 'testpassword')

    assert authenticated_user is not None
    assert authenticated_user.username == 'testuser'


@pytest.mark.django_db
def test_authenticate_failure():
    # Тестируем аутентификацию с неверными данными
    auth_service = AuthService()
    authenticated_user = auth_service.authenticate('wronguser', 'wrongpassword')

    assert authenticated_user is None


@pytest.mark.django_db
def test_authorize_admin():
    # Создаем пользователя и профиль с ролью админа
    user = User.objects.create_user(username='admin', password='admin123')
    Profile.objects.create(user=user, role='admin')

    # Тестируем авторизацию
    auth_service = AuthService()
    is_authorized = auth_service.authorize(user, 'admin')

    assert is_authorized is True


@pytest.mark.django_db
def test_authorize_doctor():
    # Создаем пользователя и профиль с ролью доктора
    user = User.objects.create_user(username='doctor', password='doctor123')
    Profile.objects.create(user=user, role='doctor')

    # Тестируем авторизацию
    auth_service = AuthService()
    is_authorized = auth_service.authorize(user, 'doctor')

    assert is_authorized is True


@pytest.mark.django_db
def test_authorize_patient():
    # Создаем пользователя и профиль с ролью пациента
    user = User.objects.create_user(username='patient', password='patient123')
    Profile.objects.create(user=user, role='patient')

    # Тестируем авторизацию
    auth_service = AuthService()
    is_authorized = auth_service.authorize(user, 'patient')

    assert is_authorized is True
