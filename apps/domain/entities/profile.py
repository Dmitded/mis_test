class Profile:
    def __init__(self, id, user_id, role, doctor_id=None, patient_id=None):
        self.id = id
        self.user_id = user_id
        self.role = role
        self.doctor_id = doctor_id
        self.patient_id = patient_id
