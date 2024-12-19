from aiogram.filters import BaseFilter
from aiogram.types import Message, MessageReactionUpdated


class ChatFilter(BaseFilter):
    async def __call__(self, update: Message | MessageReactionUpdated, chat_id: int) -> bool:
        print(update.chat.id)
        return update.chat.id == chat_id


class UsernameMessageFilter(BaseFilter):
    async def __call__(self, message: Message, username: int) -> bool:
        return f'@{username}' in message.text


class UserReactionFilter(BaseFilter):
    async def __call__(self, reaction: MessageReactionUpdated, username) -> bool:
        return reaction.user.username == username