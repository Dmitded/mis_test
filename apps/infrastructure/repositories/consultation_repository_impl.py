from typing import List
from django.db.models import Q

from apps.domain.entities.consultation import Consultation
from apps.domain.repositories.consultation_repository import ConsultationRepository
from apps.infrastructure.db.models import Consultation as ConsultationModel, Profile


class ConsultationRepositoryImpl(ConsultationRepository):
    def get_by_id(self, consultation_id: int) -> ConsultationModel:
        """Получение консультации по id

        Args:
            consultation_id (int): id консультации в БД

        Returns:
            ConsultationModel: консультация
        """
        return ConsultationModel.objects.get(id=consultation_id)

    def save(self, consultation: Consultation) -> ConsultationModel:
        """Сохранение консультации

        Args:
            consultation (Consultation): модель консультация

        Returns:
            ConsultationModel: консультация
        """
        return ConsultationModel.objects.create(
            doctor_id=consultation.doctor_id,
            patient_id=consultation.patient_id,
            created_at=consultation.created_at,
            started_at=consultation.started_at,
            finished_at=consultation.finished_at,
            status=consultation.status
        )

    def update(self, consultation_id: int, new_status: str, profile: Profile) -> ConsultationModel:
        """Обновление статуса консультации

        Args:
            consultation (ConsultationModel): консультация

        Returns:
            ConsultationModel: консультация
        """
        consultation_model = ConsultationModel.objects.filter(id=consultation_id)
        if profile.role == 'doctor':
            consultation_model = consultation_model.filter(doctor=profile.doctor)
        elif profile.role == 'patient':
            consultation_model = consultation_model.filter(doctor=profile.patient)

        consultation_model = consultation_model.get()
        consultation_model.status = new_status
        consultation_model.save()
        return consultation_model

    def delete(self, consultation_id: int):
        """Удаление консультации

        Args:
            consultation_id (int): id консультации в БД
        """
        ConsultationModel.objects.filter(id=consultation_id).delete()

    def list_all(self, filters: dict, profile: Profile) -> List[ConsultationModel]:
        """Список консультаций

        Args:
            filters (dict): фильтры запроса
            profile (Profile): запрашивающий пользователь

        Returns:
            List[ConsultationModel]: список консультаций
        """
        queryset = ConsultationModel.objects.all()
        if profile.role == 'doctor':
            queryset = queryset.filter(doctor=profile.doctor)
        elif profile.role == 'patient':
            queryset = queryset.filter(doctor=profile.patient)

        if filters:
            if filters.get('status'):
                queryset = queryset.filter(status=filters['status'])
            if filters.get('doctor_name'):
                queryset = queryset.filter(
                    Q(doctor__first_name__icontains=filters['doctor_name']) |
                    Q(doctor__last_name__icontains=filters['doctor_name']) |
                    Q(doctor__middle_name__icontains=filters['doctor_name'])
                )
            if filters.get('patient_name'):
                queryset = queryset.filter(
                    Q(patient__first_name__icontains=filters['patient_name']) |
                    Q(patient__last_name__icontains=filters['patient_name']) |
                    Q(patient__middle_name__icontains=filters['patient_name'])
                )
            if filters.get('sort_asc') == 'desc':
                queryset = queryset.order_by('-created_at')
            else:
                queryset = queryset.order_by('created_at')

        return queryset
