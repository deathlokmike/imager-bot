from dataclasses import dataclass


@dataclass
class MessageLocale:
    main: str


@dataclass
class StartMessageLocale(MessageLocale):
    choose_lang_button: str
    add_bot_to_group_button: str


@dataclass
class ScreenshotMessageLocale(MessageLocale):
    website: str
    process_time: str
    detail: str
    error: str


@dataclass
class ScreenshotData:
    explained_time: float
    title: str
    img_source: str
    url: str


@dataclass
class PageData:
    screenshot: bytes
    title: str
