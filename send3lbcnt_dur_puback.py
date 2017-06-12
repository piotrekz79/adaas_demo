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

# Turn on delivery confirmations
channel.confirm_delivery()


channel.queue_declare(queue='hello4',durable=True)

# queue is declared as durable to prevent a situation of messages being lost when a broker dies
#but to make things working messages also need to be made durable at publisher side

for i in range(1,Nmsg+1,1):
    msgbodytmp=msgbody + str(i)
    if channel.basic_publish(exchange='',
                      routing_key='hello4',
                      body=msgbodytmp,
                      properties=pika.BasicProperties(delivery_mode=2)): #but to make things working messages also need to be made durable at publisher side
        print(" [x] Sent and published %r" % msgbodytmp)
    else:
        print(" [x] Sent BUT NOT PUBLISHED %r" % msgbodytmp)

    time.sleep(1)
connection.close()

#master w.r.t. queue is the node on which queue was first time declared (Q master), NOT the master of the cluster


#Note on message persistence

#Marking messages as persistent doesn't fully guarantee that a message won't be lost.
# Although it tells RabbitMQ to save the message to disk, there is still a short time
# window when RabbitMQ has accepted a message and hasn't saved it yet.
# Also, RabbitMQ doesn't do fsync(2) for every message -- it may be just saved to
# cache and not really written to the disk. The persistence guarantees aren't strong,
#  but it's more than enough for our simple task queue.
# If you need a stronger guarantee then you can use publisher confirms.