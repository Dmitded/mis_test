from abc import ABC, abstractmethod


class ConsultationRepository(ABC):
    @abstractmethod
    def get_by_id(self, consultation_id):
        pass

    @abstractmethod
    def save(self, consultation):
        pass

    @abstractmethod
    def update(self, consultation):
        pass

    @abstractmethod
    def delete(self, consultation_id):
        pass

    @abstractmethod
    def list_all(self, filters=None, sort_by=None):
        pass
