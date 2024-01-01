from abc import abstractmethod, ABCMeta


class GenericRepository(metaclass=ABCMeta):

    @abstractmethod
    def get_by_id(self, session, _id: int):
        raise NotImplementedError

    @abstractmethod
    def commit(self, session):
        raise NotImplementedError
