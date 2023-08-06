import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
rabbitmq_client = connection.channel()
