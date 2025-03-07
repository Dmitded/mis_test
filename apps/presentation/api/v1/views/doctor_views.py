
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.presentation.api.permissions import IsAdmin
from apps.application.use_cases.doctor_use_cases import AddClinicToDoctorUseCase
from apps.infrastructure.repositories.doctor_repository_impl import DoctorRepositoryImpl
from apps.infrastructure.db.models import Clinic, Doctor


class AddClinicToDoctorView(APIView):
    permission_classes = [IsAuthenticated & IsAdmin]

    def post(self, request, doctor_id):
        clinic_id = request.data.get('clinic_id')
        try:
            use_case = AddClinicToDoctorUseCase(DoctorRepositoryImpl())
            use_case.execute(doctor_id, clinic_id)
        except Clinic.DoesNotExist:
            return Response(
                {'detail': 'Клиника не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Doctor.DoesNotExist:
            return Response(
                {'detail': 'Клиника не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                {'detail': 'Ошибка слхранения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_200_OK)
