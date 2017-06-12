#!/usr/bin/env python
import pika
import time

msgbody='Hello3 World!'
Nmsg=200

lbIP='134.221.121.65'
#lbIP='localhost'

lbPort=5670

credentials = pika.PlainCredentials('user1', 'password1')
parameters = pika.ConnectionParameters(host=lbIP, port=lbPort, virtual_host='vhost1', credentials=credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='hello3')

for i in range(1,Nmsg+1,1):
    msgbodytmp=msgbody + str(i)
    channel.basic_publish(exchange='',
                      routing_key='hello3',
                      body=msgbodytmp)
    print(" [x] Sent %r" % msgbodytmp)
    time.sleep(1)
connection.close()

#master w.r.t. queue is the node on which queue was first time declared (Q master), NOT the master of the cluster