import time

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


def all_info_callback(ch, method, properties, body):
    print(f'Received {body}')


def error_callback(ch, method, properties, body):
    print(f'Error {body}')


channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

queue_all_info = channel.queue_declare(queue='', exclusive=True)
queue_errors = channel.queue_declare(queue='', exclusive=True)
queue_all_info_name = queue_all_info.method.queue
queue_error_name = queue_errors.method.queue

for severity in ['info', 'warning', 'error']:
    channel.queue_bind(exchange='direct_logs', queue=queue_all_info_name, routing_key=severity)

channel.queue_bind(exchange='direct_logs', queue=queue_error_name, routing_key='error')

channel.basic_consume(queue=queue_all_info_name, on_message_callback=all_info_callback, auto_ack=True)
channel.basic_consume(queue=queue_error_name, on_message_callback=error_callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
