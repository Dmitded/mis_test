from django.contrib import admin
from apps.infrastructure.db.models import Profile, Doctor, Patient, Clinic, DoctorClinic, Consultation

admin.site.site_header = 'Medical Information System Admin'
admin.site.site_title = 'MIS Admin'
admin.site.index_title = 'Welcome to the Medical Information System Admin Panel'


# Регистрация модели Profile
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('id', 'user', 'role', 'doctor', 'patient')
    search_fields = ('user__username', 'role')
    list_filter = ('role',)


# Регистрация модели Doctor
class DoctorAdmin(admin.ModelAdmin):
    model = Doctor
    list_display = ('id', 'first_name', 'last_name', 'middle_name', 'specialization')
    search_fields = ('first_name', 'last_name', 'specialization')
    list_filter = ('specialization',)


# Регистрация модели Patient
class PatientAdmin(admin.ModelAdmin):
    model = Patient
    list_display = ('id', 'first_name', 'last_name', 'middle_name', 'phone', 'email')
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    list_filter = ('email',)


# Регистрация модели Clinic
class ClinicAdmin(admin.ModelAdmin):
    model = Clinic
    list_display = ('id', 'name', 'legal_address', 'physical_address')
    search_fields = ('name', 'legal_address', 'physical_address')
    list_filter = ('name',)


# Регистрация модели DoctorClinic
class DoctorClinicAdmin(admin.ModelAdmin):
    model = DoctorClinic
    list_display = ('id', 'doctor', 'clinic')
    search_fields = ('doctor__first_name', 'clinic__name')
    list_filter = ('clinic',)

    def __str__(self):
        return f'id:{self.id} доктор:{self.doctor.first_name} клиника:{self.clinic.name}'

# Регистрация модели Consultation
class ConsultationAdmin(admin.ModelAdmin):
    model = Consultation
    list_display = ('id', 'doctor', 'patient', 'started_at', 'finished_at', 'status')
    search_fields = ('doctor__first_name', 'patient__first_name')
    list_filter = ('status', 'started_at')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(DoctorClinic, DoctorClinicAdmin)
admin.site.register(Consultation, ConsultationAdmin)