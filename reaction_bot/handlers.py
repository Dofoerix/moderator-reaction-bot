import logging

from aiogram import Bot, Router, F
from aiogram.types import Message, MessageReactionUpdated

from .filters import UsernameMessageFilter, ChatFilter, UserReactionFilter


router = Router()

@router.message(F.chat.type.in_({'group', 'supergroup'}), ChatFilter(), UsernameMessageFilter())
async def username_msg(message: Message):
    await message.answer('hello, cutie')

@router.message_reaction(F.chat.type.in_({'group', 'supergroup'}), ChatFilter(), UserReactionFilter())
async def reaction(reaction: MessageReactionUpdated, bot: Bot):
    await bot.send_message(reaction.chat.id, 'wowie, ur reaction is so adorable 🥹')