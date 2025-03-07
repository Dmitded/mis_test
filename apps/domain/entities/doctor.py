class Doctor:
    def __init__(self, id, first_name, last_name, middle_name, specialization, clinic_ids=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.specialization = specialization
        self.clinic_ids = clinic_ids or []
