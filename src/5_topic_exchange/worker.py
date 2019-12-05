import time

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


def orange_animals_callback(ch, method, properties, body):
    print(f'Orange {body}')


def rabbits_and_lazy_callback(ch, method, properties, body):
    print(f'Lazy or rabbit {body}')


channel.exchange_declare(exchange='animals', exchange_type='topic')

queue_orange_animals = channel.queue_declare(queue='', exclusive=True)
queue_rabbits_and_lazy = channel.queue_declare(queue='', exclusive=True)
queue_orange_animals_name = queue_orange_animals.method.queue
queue_rabbits_and_lazy_name = queue_rabbits_and_lazy.method.queue

for topic in ['lazy.#', '*.*.rabbit']:
    channel.queue_bind(exchange='animals', queue=queue_rabbits_and_lazy_name, routing_key=topic)

channel.queue_bind(exchange='animals', queue=queue_orange_animals_name, routing_key='*.orange.*')

channel.basic_consume(queue=queue_orange_animals_name, on_message_callback=orange_animals_callback, auto_ack=True)
channel.basic_consume(queue=queue_rabbits_and_lazy_name, on_message_callback=rabbits_and_lazy_callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
