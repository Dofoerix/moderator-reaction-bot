from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    bot_token: SecretStr
    chat_id: int
    username: str
    reactions: list[str]
    prune_time: int