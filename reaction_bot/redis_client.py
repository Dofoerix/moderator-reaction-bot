import logging
import time
from datetime import datetime

from redis.asyncio import Redis


MESSAGE_IDS = 'message_ids'
RECORDS = 'records'


class RedisClient:
    def __init__(self, client: Redis, prune_time: int, records_limit: int):
        self.client = client
        self.prune_time = prune_time
        if records_limit:
            self.records_limit = records_limit
        else:
            self.records_limit = 10

    async def remove_expired(self) -> None:
        """
        Remove expired message IDs from the sorted set.
        """
        number = await self.client.zremrangebyscore('', '-inf', time.time())
        if number:
            logging.info(f'{number} messages have been pruned from the database')

    async def add_msg(self, id: int, sent_time: datetime | float | int | None = None) -> None:
        """
        Add the message ID with the expiration date score to the sorted set.
        """
        await self.remove_expired()

        if isinstance(sent_time, datetime):
            sent_timestamp = sent_time.timestamp()
        if not sent_time:
            sent_timestamp = datetime.now().timestamp()
        await self.client.zadd(MESSAGE_IDS, {id: sent_timestamp+self.prune_time})

    async def remove_msg(self, id: int) -> None:
        """
        Remove the message ID from the sorted set.
        """
        await self.remove_expired()
        await self.client.zrem(MESSAGE_IDS, id)

    async def get_msg(self, id: int) -> int | float | None:
        """
        Get the expiration date of the message with the specified ID. Return None if there is no such message ID in \
            the set.
        """
        await self.remove_expired()
        return await self.client.zscore(MESSAGE_IDS, id)

    async def add_record(self, id: int, record_time: datetime | float | int) -> bool:
        """
        Add a record to the records list. Return True if the record is a new best.
        """
        if isinstance(record_time, datetime):
            record_time = record_time.timestamp()

        # [(message_id, timestamp)]
        records: list[tuple[int, int | float]] = await self.client.zrange(RECORDS, 0, -1, withscores=True)

        if len(records) < self.records_limit:
            await self.client.zadd(RECORDS, {id: record_time})
        else:
            # Check if the last element in the records list is larger than the new one
            if records[self.records_limit-1][1] > record_time:
                await self.client.zadd(RECORDS, {id: record_time})
                await self.client.zremrangebyrank(RECORDS, self.records_limit, -1)  # Limit records to ten

        # If the added record is the first one
        if not records:
            return True
        return records[0][1] > record_time

    async def get_records(self) -> list[tuple[int, int | float]]:
        """
        Return a list of records. The first tuple element is a message ID, the second is a timestamp.
        """
        return await self.client.zrange(RECORDS, 0, self.records_limit-1, withscores=True)