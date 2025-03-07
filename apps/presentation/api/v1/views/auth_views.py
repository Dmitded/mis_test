
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.infrastructure.db.models import Profile
from apps.application.use_cases.auth_use_cases import LoginUseCase
from apps.domain.services.auth_service import AuthService


class LoginView(APIView):
    def post(self, request) -> Response:
        # Параметры запроса
        username = request.data.get('username')
        password = request.data.get('password')
        # Проверка на не пустые значения
        if not username or not password:
            return Response(
                {'detail': 'Username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            use_case = LoginUseCase(AuthService())
            user = use_case.execute(username, password)

            if user:
                profile = Profile.objects.get(user=user)
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': profile.role,
                    'doctor_id': profile.doctor_id,
                    'patient_id': profile.patient_id,
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {'detail': 'User profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {'detail': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
