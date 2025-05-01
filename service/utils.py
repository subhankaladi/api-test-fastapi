# utils.py

from fastapi import UploadFile, HTTPException
from typing import Union

class FileHandler:
    allowed_types = ["image/png", "image/jpeg", "image/jpg"]

    # Polymorphism: Method behaves differently for different files
    @classmethod
    async def read_image(cls, file: UploadFile) -> Union[bytes, None]:
        if file.content_type not in cls.allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type")
        return await file.read()
