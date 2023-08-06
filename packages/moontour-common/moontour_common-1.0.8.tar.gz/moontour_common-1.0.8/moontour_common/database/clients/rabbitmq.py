import os

import aio_pika

host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
connection = await aio_pika.connect_robust(host=host)
rabbitmq_client = connection.channel()
