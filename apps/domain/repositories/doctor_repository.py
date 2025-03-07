from abc import ABC, abstractmethod


class DoctorRepository(ABC):
    @abstractmethod
    def get_by_id(self, doctor_id):
        pass

    @abstractmethod
    def save(self, doctor):
        pass
