from domain.entities.clinic import Clinic as ClinicModel
from domain.repositories.clinic_repository import ClinicRepository


class ClinicRepositoryImpl(ClinicRepository):
    def get_by_id(self, clinic_id: int) -> ClinicModel:
        """Получение клиники

        Args:
            clinic_id (int): id клиники в БД

        Returns:
            ClinicModel: сущность клиники
        """
        return ClinicModel.objects.get(id=clinic_id)
