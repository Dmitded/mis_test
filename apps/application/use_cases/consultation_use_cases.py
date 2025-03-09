class CreateConsultationUseCase:
    def __init__(self, consultation_service):
        self.consultation_service = consultation_service

    def execute(self, consultation):
        return self.consultation_service.create_consultation(consultation)


class ListConsultationsUseCase:
    def __init__(self, consultation_repository):
        self.consultation_repository = consultation_repository

    def execute(self, filters, profile):
        return self.consultation_repository.list_all(filters=filters, profile=profile)


class UpdateConsultationStatusUseCase:
    def __init__(self, consultation_repository):
        self.consultation_repository = consultation_repository

    def execute(self, consultation_id, new_status, profile):
        return self.consultation_repository.update(consultation_id, new_status, profile)
