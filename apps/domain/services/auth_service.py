from django.contrib.auth import authenticate
from apps.infrastructure.db.models import Profile


class AuthService:
    def authenticate(self, username, password):
        """Авторизация пользователя

        Args:
            username (string): sended username
            password (string): sended password

        Returns:
            models.User: найденная сущность пользователя
        """
        user = authenticate(username=username, password=password)
        if user:
            return user
        return None

    def authorize(self, user, required_role):
        """Проверка прав доступа

        Args:
            user (models.User): сущность User
            required_role (string): роль проверки

        Returns:
            boolean (bool): Возвращает True, если у пользователя есть необходимая роль, иначе False.
        """
        profile = Profile.objects.get(user=user)
        if profile.role == 'admin':
            return True  # Админу доступно всё
        return profile.role == required_role
