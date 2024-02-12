import asyncio
import pathlib

from datetime import datetime

from bs4 import BeautifulSoup

from core.config import settings
from services.request_service import get_data_getter


async def main():
    service = await get_data_getter()
    html_text, _, _ = await service.get_text(settings.link)
    soup = BeautifulSoup(html_text, 'lxml')
    img_tag = soup.find("img")
    img_link = f"{settings.link.scheme}://{settings.link.host}/queue/{img_tag.get('src')}"
    image, headers, cookies = await service.get_content(img_link)
    await process_image(image)

    c_form = soup.find("form")
    print(c_form.find_all("input"))
    data = {e.attrs.get("name"): e.attrs.get("value") for e in c_form.find_all("input")}
    solved_captcha = input()
    data["__EVENTTARGET"] = ''
    data["__EVENTARGUMENT"] = ''
    data["ctl00$MainContent$txtCode"] = solved_captcha

    ASP_session_id = cookies.get("ASP.NET_SessionId")
    headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
   'Content-Type': 'application/x-www-form-urlencoded',
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
   'Connection': 'keep-alive',
   'Host': 'trabzon.kdmid.ru',
   'Cookie': "; ".join([f"{key}={value}" for (key, value) in cookies.items()]+[f'ASP.NET_SessionId={ASP_session_id}'])
}
    html_text, _, _ = await service.post(settings.link,
                                         data=data,
                                         headers=headers,
                                         cookies=cookies
                                         )
    soup = BeautifulSoup(html_text, 'lxml')
    c_form = soup.find("form")
    data = {e.attrs.get("name"): e.attrs.get("value") for e in c_form.find_all("input")}
    data["__EVENTTARGET"] = ''
    data["__EVENTARGUMENT"] = ''
    data["ctl00$MainContent$ButtonB.x"] = '120'
    data["ctl00$MainContent$ButtonB.y"] = '23'

    html_text, _, _ = await service.post(settings.link,
                                         data=data,
                                         headers=headers,
                                         cookies=cookies
                                         )
    soup = BeautifulSoup(html_text, 'lxml')
    await clear_tmp()
    print(soup.find("table").find("td", id="center-panel").find("p").text)


async def process_image(image: bytes) -> None:
    today = datetime.utcnow().date().isoformat()
    path = pathlib.Path.cwd().joinpath("tmp", f"{today}.jpg")
    path.touch()
    path.write_bytes(image)


async def clear_tmp() -> None:
    today = datetime.utcnow().date().isoformat()
    path = pathlib.Path.cwd().joinpath("tmp", f"{today}.jpg")
    path.unlink(missing_ok=True)

if __name__ == "__main__":
    asyncio.run(main())