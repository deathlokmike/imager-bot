import time

from selenium import webdriver

from imager_bot.services.types import PageData


class Browser:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("enable-automation")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--window-size=1600,900")
        options.add_argument("--disable-gpu")
        options.add_argument('--remote-debugging-pipe')
        self.driver = webdriver.Chrome(options=options)

    def get_screenshot(self, url: str) -> PageData:
        self.driver.get(url)
        time.sleep(0.5)  # for bad loading pages
        screenshot = self.driver.get_screenshot_as_png()
        title = self.driver.title
        domain: str = self.driver.execute_script("return document.domain;")
        domain = domain.replace("www.", "")
        self.driver.close()
        return PageData(
            screenshot=screenshot,
            title=title,
            domain=domain
        )
