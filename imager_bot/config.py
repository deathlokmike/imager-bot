from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Patterns:
    CHOOSE_LANG_CALLBACK = "choose_lang_btn"
    LANG_CALLBACK = "lang_"
    ADD_BOT_TO_GROUP_CALLBACK = "add_bot_to_group_btn"
    WHOIS_CALLBACK = "whois_btn_"


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    TG_BOT_TOKEN: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def get_database_url(self) -> str:
        return f"{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    PATTERNS = Patterns()

    @property
    def get_test_database_url(self) -> str:
        return f"{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", ignored_types=(Patterns,))


settings = Settings()
