import os
import pathlib
from pydantic_settings import BaseSettings, SettingsConfigDict
#from pydantic import SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: str
    BASE_SITE: str
    rmq_url_connection_str: str
    #ADMIN_ID: int
    model_config = SettingsConfigDict(
        env_file = f"{pathlib.Path(__file__).resolve().parent}/.env"
    )

    #def get_webhook_url(self) -> str:
        #return f"https://api.telegram.org/bot{self.BOT_TOKEN}/setWebhook?url={self.BASE_SITE}/webhook"


settings = Settings()