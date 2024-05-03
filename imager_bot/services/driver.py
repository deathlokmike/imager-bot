from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class PageData:
    screenshot: bytes
    title: str


class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.set_window_size(1366, 968)

    def get_screenshot(self, url: str) -> PageData:
        self.driver.get(url)
        screenshot = self.driver.get_screenshot_as_png()
        title = self.driver.title
        self.driver.close()
        return PageData(
            screenshot=screenshot,
            title=title
        )
