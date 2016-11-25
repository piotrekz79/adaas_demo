#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello22')

channel.basic_publish(exchange='',
                      routing_key='hello22',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
