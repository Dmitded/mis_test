from apps.domain.repositories.doctor_repository import DoctorRepository
from apps.infrastructure.db.models import Doctor as DoctorModel, DoctorClinic
from apps.domain.entities.doctor import Doctor


class DoctorRepositoryImpl(DoctorRepository):
    def get_by_id(self, doctor_id: int) -> Doctor:
        """Получение доктора

        Args:
            doctor_id (int): id доктора в БД

        Returns:
            Doctor: доктор
        """
        doctor = DoctorModel.objects.get(id=doctor_id)
        clinic_ids = list(DoctorClinic.objects.filter(doctor=doctor).values_list('clinic_id', flat=True))
        return Doctor(
            id=doctor.id,
            first_name=doctor.first_name,
            last_name=doctor.last_name,
            middle_name=doctor.middle_name,
            specialization=doctor.specialization,
            clinic_ids=clinic_ids
        )

    def save(self, doctor: Doctor) -> DoctorModel:
        """Сохранение доктора

        Args:
            doctor (Doctor): доктор

        Returns:
            DoctorModel: доктор
        """
        doctor_model, _ = DoctorModel.objects.get_or_create(
            id=doctor.id,
            defaults={
                'first_name': doctor.first_name,
                'last_name': doctor.last_name,
                'middle_name': doctor.middle_name,
                'specialization': doctor.specialization
            }
        )
        for clinic_id in doctor.clinic_ids:
            DoctorClinic.objects.get_or_create(doctor=doctor_model, clinic_id=clinic_id)
        return doctor_model
