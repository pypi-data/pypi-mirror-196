import os

import aio_pika
from aio_pika import Message
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractQueue, ExchangeType, \
    AbstractRobustChannel

from moontour_common.models import BaseRoom

ROOMS_EXCHANGE_NAME = 'rooms'


async def get_rabbitmq_client() -> AbstractRobustChannel:
    host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    connection = await aio_pika.connect_robust(host=host)
    return await connection.channel()


async def declare_rooms_exchange(channel: AbstractChannel) -> AbstractExchange:
    return await channel.declare_exchange(name=ROOMS_EXCHANGE_NAME, type=ExchangeType.TOPIC)


async def declare_player_queue(channel: AbstractChannel, rooms_exchange: AbstractExchange, room_id: str,
                               user_id: str) -> AbstractQueue:
    queue_name = f'{room_id}.{user_id}'
    queue = await channel.declare_queue(name=queue_name, auto_delete=True)
    await queue.bind(rooms_exchange, routing_key=f'{room_id}.*')
    return queue


async def notify_room(exchange: AbstractExchange, room: BaseRoom):
    await exchange.publish(
        message=Message(body=room.json().encode()),
        routing_key=f'{room.id}.*',
    )
