from abc import ABC, abstractmethod


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