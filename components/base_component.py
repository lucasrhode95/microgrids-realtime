from abc import ABC, abstractmethod
from dataclasses import dataclass

from communication.io_manager import IOManager


@dataclass
class BaseComponent(ABC):
    io_client: IOManager
    rt_manager: 'BaseManager' = None

    @abstractmethod
    def next_step(self, t: float, previous_output: any) -> any:
        raise NotImplementedError()

    def initialize(self, t0: float) -> any:
        pass


from managers.base_manager import BaseManager
