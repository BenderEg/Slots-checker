from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):

    host: str
    port: int
    db: int


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file='../../.env',
                                      env_file_encoding='utf-8',
                                      env_nested_delimiter='__'
                                      )
    token: str
    link: HttpUrl
    redis: RedisSettings
    owner_id: int
    time: list

settings = Settings()