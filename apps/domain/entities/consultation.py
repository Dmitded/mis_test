class Consultation:
    def __init__(self, id, doctor_id, patient_id, created_at, started_at, finished_at, status):
        self.id = id
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.created_at = created_at
        self.started_at = started_at
        self.finished_at = finished_at
        self.status = status
