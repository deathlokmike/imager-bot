import time

import httpx
import validators

from imager_bot.database.dao.users import UsersDaO
from imager_bot.services.driver import Browser
from imager_bot.services.exceptions import UploadException, ValidationException
from imager_bot.services.translator import Translator
from imager_bot.services.types import ScreenshotData, ScreenshotMessageLocale


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
    def validate_url(cls, _url: str) -> str:
        if not validators.url(_url):
            _url = f'http://' + _url
            if not validators.url(_url):
                raise ValidationException
        return _url

    @classmethod
    async def get_data(cls, url: str) -> ScreenshotData:
        start_ = time.time()
        page_data = Browser().get_screenshot(url)
        explained_time = time.time() - start_
        src = await upload_image_to_telegraph(page_data.screenshot)
        return ScreenshotData(
            explained_time=explained_time,
            title=page_data.title,
            img_source=f'https://telegra.ph{src}',
            url=url
        )

    @classmethod
    async def get_locales(cls, tg_id: int) -> ScreenshotMessageLocale:
        user = await UsersDaO.get_by_id(tg_id)
        translator = Translator(user.locale)
        locale: ScreenshotMessageLocale = translator.get_translate("screenshot", ScreenshotMessageLocale)

        return locale
