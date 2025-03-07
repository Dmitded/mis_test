import pytest
from apps.infrastructure.repositories.profile_repository_impl import ProfileRepositoryImpl
from apps.infrastructure.db.models import Profile as ProfileModel, User


@pytest.mark.django_db
def test_get_by_user_id():
    # Создаем пользователя и профиль
    user = User.objects.create_user(username='testuser', password='testpassword')
    profile = ProfileModel.objects.create(user=user, role='admin')

    # Тестируем получение профиля по user_id
    profile_repository = ProfileRepositoryImpl()
    result = profile_repository.get_by_user_id(user.id)

    assert result is not None
    assert result.id == profile.id
    assert result.user_id == user.id
    assert result.role == 'admin'
