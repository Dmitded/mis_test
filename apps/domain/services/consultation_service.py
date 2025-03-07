class ConsultationService:

    def __init__(self, consultation_repository):
        """init function

        Args:
            consultation_repository (ConsultationRepository):
            инициализация работы с сущностью БД consultation
        """
        self.consultation_repository = consultation_repository

    def create_consultation(self, consultation):
        """Создание консультации

        Args:
            consultation (models.Consultation): объект класса Consultation

        Returns:
            models.Consultation: сохраненная сущность консультации
        """
        return self.consultation_repository.save(consultation)

    def update_consultation(self, consultation):
        """Обновление консультации

        Args:
            consultation (models.Consultation): объект класса Consultation

        Returns:
            models.Consultation: сохраненная сущность консультации
        """
        return self.consultation_repository.update(consultation)

    def delete_consultation(self, consultation_id):
        """Удаление консультации

        Args:
            consultation_id (integer): id консультации в БД

        Returns:
            result(tuple[int, dict[str, int]]): результат удаления
        """
        return self.consultation_repository.delete(consultation_id)

    def get_consultation(self, consultation_id):
        """Получение консультаии

        Args:
            consultation_id (integer): id консультации в БД

        Returns:
            Consultation: сущность консультации
        """
        return self.consultation_repository.get_by_id(consultation_id)

    def list_consultations(self, filters):
        """Получение списка консультаций

        Args:
            filters (dict): список фильтро в формате key:value

        Returns:
            list(models.Consultation): список консультаций
        """
        return self.consultation_repository.list_all(filters)
