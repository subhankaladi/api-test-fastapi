# base.py
from abc import ABC, abstractmethod

# Abstraction (Abstract Class)
class BaseProcessor(ABC):

    @abstractmethod
    def remove_background(self, image_bytes: bytes) -> bytes:
        pass
