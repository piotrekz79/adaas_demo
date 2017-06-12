#!/usr/bin/env python
import pika
lbIP='134.221.121.65'
#lbIP='localhost'

lbPort=5670

credentials = pika.PlainCredentials('user1', 'password1')
parameters = pika.ConnectionParameters(host=lbIP, port=lbPort, virtual_host='vhost1', credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello3')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello3',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

#no ACK - if consumer dies, messages are lost