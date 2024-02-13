from abc import ABC, abstractmethod

from pathlib import Path

class AbstractContentGetter(ABC):

    @abstractmethod
    async def get_text(self, url: str, headers: dict,
                       data: dict, cookies: dict)-> tuple[str, dict, dict]:
        pass

    @abstractmethod
    async def get_content(self, url: str, headers: dict,
                          data: dict, cookies: dict) -> tuple[str, dict, dict]:
        pass


    @abstractmethod
    async def post(self, url: str, headers: dict,
                   data: dict, cookies: dict) -> tuple[str, dict, dict]:
        pass


class AbstractImageService(ABC):

    path: Path

    @abstractmethod
    def save_image(self, image: bytes)-> None:
        pass

    @abstractmethod
    def delete_image(self) -> None:
        pass
