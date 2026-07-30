from pydantic_settings import BaseSettings

from drawthings_openai.constants import (
    DEFAULT_IMAGE_SERVER_TARGET,
    DEFAULT_INSECURE_SERVER,
    DEFAULT_TIMEOUT_SECONDS,
)

class Settings(BaseSettings):
    server_target: str = DEFAULT_IMAGE_SERVER_TARGET
    server_timeout: float = DEFAULT_TIMEOUT_SECONDS
    insecure_server: bool = DEFAULT_INSECURE_SERVER

    model_config = {"env_file": ".env"}

settings = Settings()
