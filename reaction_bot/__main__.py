import asyncio
import logging

from aiogram import Bot, Dispatcher

from .config import Config
from .handlers import router


async def main():
    logging.basicConfig(format='%(levelname)s | %(message)s', level=logging.INFO)

    config = Config()

    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher(chat_id=config.chat_id, username=config.username, reactions=config.reactions)
    dp.include_routers(router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())