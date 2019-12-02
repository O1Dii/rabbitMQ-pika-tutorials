import sys

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

message = ' '.join(sys.argv[2:]) or 'Hello World!'
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)

print(f"Sent '{message}'")

connection.close()
