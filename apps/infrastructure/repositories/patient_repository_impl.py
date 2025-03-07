from apps.domain.repositories.patient_repository import PatientRepository
from apps.infrastructure.db.models import Patient as PatientModel
from apps.domain.entities.patient import Patient


class PatientRepositoryImpl(PatientRepository):
    def get_by_id(self, patient_id: int) -> Patient:
        """Получение пациента

        Args:
            patient_id (int): id пациента в БД

        Returns:
            Patient: пациент
        """
        patient = PatientModel.objects.get(id=patient_id)
        return Patient(
            id=patient.id,
            first_name=patient.first_name,
            last_name=patient.last_name,
            middle_name=patient.middle_name,
            phone=patient.phone,
            email=patient.email
        )

    def save(self, patient: Patient) -> PatientModel:
        """Сохранение пациента

        Args:
            patient (Patient): пациент

        Returns:
            PatientModel: пациент
        """
        patient_model, _ = PatientModel.objects.get_or_create(
            id=patient.id,
            defaults={
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'middle_name': patient.middle_name,
                'phone': patient.phone,
                'email': patient.email
            }
        )
        return patient_model
