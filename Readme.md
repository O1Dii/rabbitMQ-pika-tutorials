# RabbitMQ

RabbitMQ is a message broker: it accepts and forwards messages. 

X - exchange (it decides, where to send your message)  
Red bars - queues (stores messages until client handles them)

![](https://www.rabbitmq.com/img/tutorials/python-three-overall.png)

### **There are 5 types of exchanges in rabbitmq:**
* default, it derives messages by queue names
* fanout, it sends messages to all queues  
![](https://lostechies.com/content/derekgreer/uploads/2012/03/FanoutExchange_thumb2.png)  
* direct  
![](https://lostechies.com/content/derekgreer/uploads/2012/03/DirectExchange_thumb1.png)  
* topic  
![](https://lostechies.com/content/derekgreer/uploads/2012/03/TopicExchange_thumb2.png)  
* headers  
![](https://lostechies.com/content/derekgreer/uploads/2012/03/HeadersExchange_thumb2.png)  

### **Message acknowledgments:**
acknowledgment is used to prevent messages lost due to client crushing. If ack is enabled, client needs to send special messages back to the server for it to know that message got delivered. If server doesn't receive this message, it re-queues main message.

### **If RabbitMQ server stops working:**
by default, if rabbitmq server stops working, all messages and queues are lost, but we can change it by making them "durable". To make messages durable, we need to set their delivery_mode to 2 in properties.

### **Fair dispatch:**
by default rabbitmq dispatches messages from one queue to next consumer, it doesn't watch, if it's ready to handle the message or no. We can change this behaviour by setting prefetch count. Prefetch count (int) shows how many messages can one subscriber handle at a time.  
![](https://habrastorage.org/storage2/f0e/b4d/c62/f0eb4dc626e5da02d78a49fc05536b34.png)
> channel.basic_qos(prefetch_count=1)

### **RPC:**
Remote Procedure Call  
To get it working, server needs to send responses -> it needs to know, where to send, so we add "reply_to" and "correlation_id' to request props. reply_to - queue_name, correlation_id - unique identifier to prevent suitable, but inappropriate queues to get response

### **Basic operations:**
**Sender:**
* Declare connection  
> connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

* Get chanel  
> channel = connection.channel()

* Declare exchange  
> channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

* Send message  
> channel.basic_publish(exchange=exchange_name, routing_key=your_routing_key, body=message)

* Close connection  
> connection.close()

**Receiver:**
* Declare connection  
> connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

* Get chanel  
> channel = connection.channel()

* Declare exchange  
> channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

* Declare queue
> result = channel.queue_declare(queue=queue_name, exclusive=True) # queue_name can be an empty string -> get_queue_name: result.method.queue

* Write callback function
> def callback(ch, method, props, body): ...

* Bind queue to exchange
> channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key) # no need in routing_key with fanout exchange

* Bind callback to queue
> channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True) # auto_ack=True -> ack off. If on, then callback must have ch.basic_ack(delivery_tag=method.delivery_tag)

* Start loop
> channel.start_consuming()
