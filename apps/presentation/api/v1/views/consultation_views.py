from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.presentation.api.permissions import IsAdmin, IsDoctor, IsPatient
from apps.presentation.api.v1.serializers.consultation_serializers import ConsultationSerializer
from apps.application.use_cases.consultation_use_cases import ListConsultationsUseCase, UpdateConsultationStatusUseCase
from apps.infrastructure.repositories.consultation_repository_impl import ConsultationRepositoryImpl
from apps.infrastructure.db.models import Consultation


class ListConsultationsView(APIView):
    permission_classes = [IsAuthenticated & (IsAdmin | IsDoctor | IsPatient)]

    def get(self, request):
        # Параметры запроса
        filters = {
            'status': request.query_params.get('status', None),
            'doctor_name': request.query_params.get('doctor_name', None),
            'patient_name': request.query_params.get('patient_name', None),
            'sort_asc': request.query_params.get('sort_asc', None),
        }

        use_case = ListConsultationsUseCase(ConsultationRepositoryImpl())
        consultations = use_case.execute(filters)

        # Сериализация данных
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateConsultationStatusView(APIView):
    permission_classes = [IsAuthenticated & (IsAdmin | IsDoctor)]

    def patch(self, request, consultation_id):
        new_status = request.data.get('status')
        # Получаем консультацию
        try:
            consultation = Consultation.objects.get(id=consultation_id)
        except Consultation.DoesNotExist:
            return Response(
                {'detail': 'Консультация не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )
        # проверка валидности переданного статуса
        valid_statuses = [choice[0] for choice in Consultation.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {'detail': f'Недопустимый статус. Допустимые статусы: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        use_case = UpdateConsultationStatusUseCase(ConsultationRepositoryImpl())
        consultation = use_case.execute(consultation_id, new_status)

        # Сериализация данных
        serializer = ConsultationSerializer(consultation)
        return Response(serializer.data, status=status.HTTP_200_OK)
