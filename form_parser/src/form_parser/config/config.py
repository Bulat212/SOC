from pydantic_settings import BaseSettings, SettingsConfigDict

class RabbitSOCSettings(BaseSettings):
    url: str

    model_config = SettingsConfigDict(
        env_prefix="RABBIT_SOC_",
        env_file=".env",     
        env_file_encoding="utf-8"
    )