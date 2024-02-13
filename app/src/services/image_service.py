from datetime import datetime
from pathlib import Path

from services.abstract import AbstractImageService

class ImageService(AbstractImageService):

    def __init__(self) -> None:
        self.path = None

    def save_image(self, image: bytes)-> None:
        today = datetime.utcnow().date().isoformat()
        path = Path.cwd().joinpath("tmp", f"{today}.jpeg")
        path.touch()
        path.write_bytes(image)
        self.path = path

    def delete_image(self) -> None:
        self.path.unlink(missing_ok=True)
        self.path = None
