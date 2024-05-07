import time

import httpx
import validators
from selenium.common.exceptions import WebDriverException

from imager_bot.database.dao.stats import UsersStatisticsDaO
from imager_bot.database.dao.users import UsersDaO
from imager_bot.services.driver import Browser
from imager_bot.services.exceptions import UploadException, ValidationException
from imager_bot.services.translator import Translator
from imager_bot.services.types import ScreenshotData, ScreenshotMessageLocale
from imager_bot.services.whois import get_whois_text


async def upload_image_to_telegraph(image: bytes) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url='https://telegra.ph/upload',
            files={'file': ('file', image, 'image/png')})
        if response.status_code == 200:
            json_ = response.json()[0]
            return json_.get("src")
        else:
            raise UploadException


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
        try:
            return cls._validate_message(message)
        except ValidationException:
            await UsersStatisticsDaO.increase_bad_request(tg_id)
            raise ValidationException

    @classmethod
    async def get_data(cls, url: str, tg_id: int) -> ScreenshotData:
        start_ = time.time()
        try:
            page_data = Browser().get_screenshot(url)
            explained_time = time.time() - start_
            src = await upload_image_to_telegraph(page_data.screenshot)
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
