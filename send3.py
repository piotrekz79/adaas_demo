#!/usr/bin/env python
import pika

msgbody='Hello3 World!'

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',port=5670))
channel = connection.channel()

channel.queue_declare(queue='hello3')

channel.basic_publish(exchange='',
                      routing_key='hello3',
                      body=msgbody)
print(" [x] Sent %r" % msgbody)
connection.close()

#master w.r.t. queue is the node on which queue was first time declared (Q master), NOT the master of the cluster