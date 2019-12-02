import sys

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='animals', exchange_type='topic')

message = ' '.join(sys.argv[2:]) or 'arh-wooooo!'
topic = sys.argv[1] if len(sys.argv) > 1 else 'lazy.orange.rabbit'
channel.basic_publish(exchange='animals', routing_key=topic, body=message)

print(f"Sent '{message}'")

connection.close()
