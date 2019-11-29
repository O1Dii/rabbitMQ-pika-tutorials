import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

message = 'Hi!'
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

print(f"Sent '{message}'")

connection.close()
