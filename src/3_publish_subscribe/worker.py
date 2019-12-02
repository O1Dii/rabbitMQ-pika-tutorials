import time

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)


def callback(ch, method, properties, body):
    print(f'Received {body}')


channel.queue_bind(exchange='logs', queue=result.method.queue)

channel.basic_consume(queue=result.method.queue, on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
