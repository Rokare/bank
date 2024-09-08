from abc import ABC, abstractmethod


class BaseDao(ABC):

    @abstractmethod
    def create(self, dict):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def get_all(self):
        pass


class FullBaseDao(BaseDao):

    @abstractmethod
    def modify(id: int, dict):
        pass

    @abstractmethod
    def delete_by_id(id: int):
        pass

    @abstractmethod
    def delete_all(self):
        pass
