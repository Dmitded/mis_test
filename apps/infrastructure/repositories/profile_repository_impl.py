from apps.domain.entities.profile import Profile
from apps.domain.repositories.profile_repository import ProfileRepository
from apps.infrastructure.db.models import Profile as ProfileModel


class ProfileRepositoryImpl(ProfileRepository):
    def get_by_user_id(self, user_id: int) -> Profile:
        """Получение профиля по user_id

        Args:
            user_id (int): id пользователя в БД

        Returns:
            Profile: профиль
        """
        try:
            profile = ProfileModel.objects.get(user_id=user_id)
            return Profile(
                id=profile.id,
                user_id=profile.user_id,
                role=profile.role,
                doctor_id=profile.doctor_id,
                patient_id=profile.patient_id,
            )
        except ProfileModel.DoesNotExist:
            return None
