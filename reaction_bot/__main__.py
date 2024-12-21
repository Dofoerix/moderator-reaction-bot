import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from redis.asyncio import Redis

from .config import Config
from .handlers import router
from .redis_client import RedisClient


async def main():
    logging.basicConfig(format='%(levelname)s | %(message)s', level=logging.INFO)

    config = Config()

    redis_client = RedisClient(
        Redis(host=config.redis_host, port=config.redis_port, decode_responses=True),
        config.prune_time,
        config.records_limit
    )
    await redis_client.remove_expired()

    bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(link_preview_is_disabled=True))
    dp = Dispatcher(chat_id=config.chat_id, username=config.username, reactions=config.reactions, redis=redis_client)
    dp.include_routers(router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())