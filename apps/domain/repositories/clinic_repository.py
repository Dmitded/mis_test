from abc import ABC, abstractmethod


class ClinicRepository(ABC):
    @abstractmethod
    def get_by_id(self, clinic_id):
        pass

    @abstractmethod
    def save(self, clinic):
        pass
