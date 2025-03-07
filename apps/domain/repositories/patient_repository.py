from abc import ABC, abstractmethod


class PatientRepository(ABC):
    @abstractmethod
    def get_by_id(self, patient_id):
        pass

    @abstractmethod
    def save(self, patient):
        pass
