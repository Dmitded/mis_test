from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.presentation.api.v1.views.consultation_views import ListConsultationsView, UpdateConsultationStatusView
from apps.presentation.api.v1.views.doctor_views import AddClinicToDoctorView
from apps.presentation.api.v1.views.auth_views import LoginView


urlpatterns = [
    path('auth', LoginView.as_view(), name='token_obtain_pair'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('doctors/<int:doctor_id>/add_clinic', AddClinicToDoctorView.as_view(), name='add_clinic_to_doctor'),
    path('consultations', ListConsultationsView.as_view(), name='list_consultations'),
    path('consultations/<int:consultation_id>/status', UpdateConsultationStatusView.as_view(), name='update_consultation_status'),
]
