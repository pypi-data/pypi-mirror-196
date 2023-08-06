import os

import aio_pika

host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
rabbitmq_client = await aio_pika.connect_robust(host=host)
