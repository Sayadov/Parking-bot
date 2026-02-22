from abc import ABC, abstractmethod


class IS3Driver(ABC):
    @abstractmethod
    def get_object(self, bucket: str, key: str):
        pass

    @abstractmethod
    def put_object(self, bucket: str, key: str, body: str, etag: str = None):
        pass
