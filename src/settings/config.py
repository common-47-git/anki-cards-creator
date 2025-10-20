from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )

    @classmethod
    def load(cls) -> "ConfigBase":
        return cls()


class EnToEnConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="EN_TO_EN_")

    PATH: str
    DECK: str


class Config(BaseSettings):
    en_to_en: EnToEnConfig = Field(default_factory=EnToEnConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()
