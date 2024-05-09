import asyncio
import os
import time
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
import validators
from selenium.common.exceptions import WebDriverException

from imager_bot.database.dao.stats import UsersStatisticsDaO
from imager_bot.database.dao.users import UsersDaO
from imager_bot.services.driver import Browser
from imager_bot.services.exceptions import UploadException, ValidationException
from imager_bot.services.translator import Translator
from imager_bot.services.types import ScreenshotData, ScreenshotMessageLocale
from imager_bot.services.users import UsersService
from imager_bot.services.utils import naive_utcnow
from imager_bot.services.whois import get_whois_text

if TYPE_CHECKING:
    from imager_bot.services.types import PageData


async def _upload_image_to_telegraph(image: bytes) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url='https://telegra.ph/upload',
            files={'file': ('file', image, 'image/png')})
        if response.status_code == 200:
            json_ = response.json()[0]
            return json_.get("src")
        else:
            raise UploadException


def _screenshot_task(url: str) -> "PageData":
    return Browser().get_screenshot(url)


def _save_screenshot(tg_id: int, domain: str, image: bytes):
    home = Path.home()
    date = datetime.strftime(naive_utcnow(), '%d-%m-%y-%H-%M-%S')
    cache = os.path.join(home, ".cache", "imager_bot")
    if not os.path.exists(cache):
        os.mkdir(cache)
    image_path = f"{date}_{tg_id}_{domain}.png"
    with open(os.path.join(cache, image_path), "wb") as f:
        f.write(image)


async def _execute_screenshot_task(url: str) -> "PageData":
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        call = partial(_screenshot_task, url)
        tasks = [loop.run_in_executor(process_pool, call)]
        results = await asyncio.gather(*tasks)
        for result in results:
            return result


class ScreenshotService:

    @classmethod
    def _validate_message(cls, message: str) -> str:
        if not validators.url(message):
            message = f'http://' + message
            if not validators.url(message):
                raise ValidationException
        return message

    @classmethod
    async def get_url(cls, message: str, tg_id: int) -> str:
        await UsersService.validate_user(tg_id)
        try:
            return cls._validate_message(message)
        except ValidationException:
            await UsersStatisticsDaO.increase_bad_request(tg_id)
            raise ValidationException

    @classmethod
    async def get_data(cls, url: str, tg_id: int) -> ScreenshotData:
        start_ = time.time()
        try:
            page_data = await _execute_screenshot_task(url)
            explained_time = time.time() - start_
            src = await _upload_image_to_telegraph(page_data.screenshot)
            _save_screenshot(tg_id, page_data.domain, page_data.screenshot)
            await UsersStatisticsDaO.increase_screenshot(tg_id)
            return ScreenshotData(
                explained_time=explained_time,
                title=page_data.title,
                img_source=f'https://telegra.ph{src}',
                url=url,
                domain=page_data.domain
            )
        except (WebDriverException, UploadException) as exc:
            await UsersStatisticsDaO.increase_bad_request(tg_id)
            raise exc

    @classmethod
    async def get_locales(cls, tg_id: int) -> ScreenshotMessageLocale:
        user = await UsersDaO.get_by_id(tg_id)
        translator = Translator(user.locale)
        locale: ScreenshotMessageLocale = translator.get_translate("screenshot", ScreenshotMessageLocale)

        return locale

    @classmethod
    async def get_whois_data(cls, domain: str, tg_id: int) -> str:
        w = await get_whois_text(domain)
        await UsersStatisticsDaO.increase_whois_request(tg_id)
        return w
