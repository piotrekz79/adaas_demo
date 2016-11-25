#!/usr/bin/env python
import pika

msgbody='Hello3 World!'

lbIP='134.221.121.65'
#lbIP='localhost'

lbPort=5670

credentials = pika.PlainCredentials('user1', 'password1')
parameters = pika.ConnectionParameters(host=lbIP, port=lbPort, virtual_host='vhost1', credentials=credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='hello3')

channel.basic_publish(exchange='',
                      routing_key='hello3',
                      body=msgbody)
print(" [x] Sent %r" % msgbody)
connection.close()

#master w.r.t. queue is the node on which queue was first time declared (Q master), NOT the master of the cluster