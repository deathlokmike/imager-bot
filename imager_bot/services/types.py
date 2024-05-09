from dataclasses import dataclass


@dataclass
class MessageLocale:
    main: str


@dataclass
class StartMessageLocale(MessageLocale):
    choose_lang_button: str


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
    domain: str


@dataclass
class PageData:
    screenshot: bytes
    title: str
    domain: str
