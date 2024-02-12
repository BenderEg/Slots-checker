from services.abstract import AbstractContentGetter

import requests


class DataGetter(AbstractContentGetter):

    async def get_text(self,
                       url: str,
                       headers: dict = {},
                       data: dict = {},
                       cookies: dict = {}
                       ) -> tuple[str, dict, dict]:
        response = requests.get(url, headers=headers,
                                json=data, cookies=cookies)
        return response.text, response.headers, response.cookies.get_dict()

    async def get_content(self,
                          url: str,
                          headers: dict = {},
                          data: dict = {},
                          cookies: dict = {}
                          ) -> tuple[str, dict, dict]:
        response = requests.get(url, headers=headers,
                                json=data, cookies=cookies)
        return response.content, response.headers, response.cookies.get_dict()

    async def post(self,
                   url: str,
                   headers: dict = {},
                   data: dict = {},
                   cookies: dict = {}
                   ) -> tuple[str, dict, dict]:
        response = requests.post(url,
                                 data=data,
                                 headers=headers,
                                 cookies=cookies
                                 )
        return response.text, response.headers, response.cookies.get_dict()


async def get_data_getter() -> DataGetter:
    return DataGetter()