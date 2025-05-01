# remover.py

from rembg import remove
from .base import BaseProcessor

# Inheritance + Encapsulation
class BackgroundRemover(BaseProcessor):
    def __init__(self):
        self.name = "RembgProcessor"

    def remove_background(self, image_bytes: bytes) -> bytes:
        # Encapsulation: processing logic hidden inside method
        result = remove(image_bytes)
        return result
