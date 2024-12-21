from aiogram.filters import BaseFilter
from aiogram.types import Message, MessageReactionUpdated

from .redis_client import RedisClient


class ChatFilter(BaseFilter):
    async def __call__(self, update: Message | MessageReactionUpdated, chat_id: int) -> bool:
        return update.chat.id == chat_id


class UsernameMessageFilter(BaseFilter):
    async def __call__(self, message: Message, username: str) -> bool:
        if message.text:
            message_text = message.text
        else:
            if message.caption:
                message_text = message.caption
            else:
                message_text = ''

        return f'@{username}'.lower() in message_text.lower()


class UserReactionFilter(BaseFilter):
    async def __call__(
            self,
            reaction: MessageReactionUpdated,
            username: str,
            reactions: list[str],
            redis: RedisClient
    ) -> bool:
        if reaction.new_reaction:
            return (
                reaction.user.username and
                reaction.user.username.lower() == username.lower() and
                reaction.new_reaction[0].emoji in reactions and
                await redis.get_msg(reaction.message_id)
            )
        return False