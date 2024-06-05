import logging
import httpx
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cmw_base_url: str = "http://localhost:8081/cmw"
    cmw_auth_token: str = "test-token"
    cmw_read_only: bool = True

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
logger = logging.getLogger("uvicorn.error")


def get_subscription(id: int):
    url = f"{settings.cmw_base_url}/subscription/{id}"
    headers = {"CMW-Auth-Token": settings.cmw_auth_token}
    r = httpx.get(url, headers=headers)
    return r.raise_for_status().json()


def update_status(subscription_id: int, status: str):
    logger.info("Setting subscription %s to %s", subscription_id, status)

    if settings.cmw_read_only:
        return

    url = f"{settings.cmw_base_url}/subscription/{id}"
    headers = {"CMW-Auth-Token": settings.cmw_auth_token}
    httpx.patch(url, headers=headers, json={"deploymentStatus": status})
