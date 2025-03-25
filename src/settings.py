from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    API_SCHEMA: str = Field(default="http")
    API_HOST: str = Field(default="localhost")
    API_PORT: int = Field(default=5000)

    @property
    def core_api_endpoint(self) -> str:
        return f"{self.API_SCHEMA}://{self.API_HOST}:{self.API_PORT}"

    KAFKA_BOOTSTRAP_SERVERS: str = Field(default="localhost:29092")

    BOT_TOKEN: str = Field(default="")
    GITHUB_ACCESS_TOKEN: str = Field(default="")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


app_settings = AppSettings()
