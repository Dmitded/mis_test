from abc import ABC, abstractmethod


class ProfileRepository(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id):
        pass
