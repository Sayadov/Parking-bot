from abc import ABC, abstractmethod
from packages.entites.state import State


class IS3Adapter(ABC):
    @abstractmethod
    def download(self) -> State:
        pass

    @abstractmethod
    def upload(self, state: State):
        pass
