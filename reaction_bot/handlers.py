import logging

from aiogram import Bot, Router, F
from aiogram.types import Message, MessageReactionUpdated
from aiogram.filters import Command
from aiogram.utils import formatting as form

from .filters import UsernameMessageFilter, ChatFilter, UserReactionFilter
from .redis_client import RedisClient
from .utils import format_time


router = Router()
router.message.filter(ChatFilter(), F.chat.type.in_({'group', 'supergroup'}))

@router.message(UsernameMessageFilter())
async def username_msg(message: Message, redis: RedisClient):
    await redis.add_msg(message.message_id, message.date)
    logging.info(f'Message {message.message_id} in chat {message.chat.id} has been added to the database')

@router.message_reaction(F.chat.type.in_({'group', 'supergroup'}), ChatFilter(), UserReactionFilter())
async def reaction(reaction: MessageReactionUpdated, bot: Bot, redis: RedisClient, username: str):
    message_time = await redis.get_msg(reaction.message_id) - redis.prune_time
    reaction_time = reaction.date.timestamp()
    record_time = reaction_time - message_time

    await redis.remove_msg(reaction.message_id)
    logging.info(f'Message {reaction.message_id} in chat {reaction.chat.id} has been removed from the database')

    if await redis.add_record(reaction.message_id, record_time):
        new_best = form.Bold('Новый рекорд!\n')
    else:
        new_best = ''

    answer = form.Text(
        new_best,
        form.TextLink('Модератор', url=f'https://t.me/{username}'),
        (
            f' справился за {format_time(record_time)}\n'
            'Чтобы просмотреть рекорды, используйте команду /records'
        )
    )

    await bot.send_message(reaction.chat.id, **answer.as_kwargs(), reply_to_message_id=reaction.message_id)

@router.message(Command('records'))
async def records(message: Message, redis: RedisClient, username: str):
    # [(message_id, timestamp)]
    records = await redis.get_records()

    moderator = form.TextLink('модератора', url=f'https://t.me/{username}')

    if records:
        formatted_answer = []
        for record in records:
            if message.chat.username:
                chat_id = message.chat.username
            else:
                chat_id = f'c/{str(message.chat.id).lstrip('-100')}'
            formatted_answer.append(
                form.TextLink(f'{format_time(record[1])}', url=f'https://t.me/{chat_id}/{record[0]}')
            )
        answer = form.as_numbered_section(
            form.Bold('Список рекордов ', moderator, ':'),
            *formatted_answer
        )
    else:
        answer = form.Text('У ', moderator, ' нет рекордов 😔')

    await message.reply(**answer.as_kwargs())