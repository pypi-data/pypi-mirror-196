import os

import aio_pika
from aio_pika.abc import AbstractRobustConnection


async def get_rabbitmq_client() -> AbstractRobustConnection:
    host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    return await aio_pika.connect_robust(host=host)
