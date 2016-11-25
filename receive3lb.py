#!/usr/bin/env python
import pika
lbIP='134.221.121.65'
lbPort=5670

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=lbIP,port=lbPort))
channel = connection.channel()

channel.queue_declare(queue='hello3')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello3',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()