class AddClinicToDoctorUseCase:
    def __init__(self, doctor_repository):
        self.doctor_repository = doctor_repository

    def execute(self, doctor_id, clinic_id):
        doctor = self.doctor_repository.get_by_id(doctor_id)
        doctor.clinic_ids.append(clinic_id)
        self.doctor_repository.save(doctor)
