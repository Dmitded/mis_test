class CreateConsultationUseCase:
    def __init__(self, consultation_service):
        self.consultation_service = consultation_service

    def execute(self, consultation):
        return self.consultation_service.create_consultation(consultation)


class ListConsultationsUseCase:
    def __init__(self, consultation_repository):
        self.consultation_repository = consultation_repository

    def execute(self, filters={}):
        return self.consultation_repository.list_all(filters=filters)


class UpdateConsultationStatusUseCase:
    def __init__(self, consultation_repository):
        self.consultation_repository = consultation_repository

    def execute(self, consultation_id, new_status):
        consultation = self.consultation_repository.get_by_id(consultation_id)
        consultation.status = new_status
        return self.consultation_repository.update(consultation)
