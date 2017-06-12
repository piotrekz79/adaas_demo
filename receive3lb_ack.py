#!/usr/bin/env python
import pika
lbIP='134.221.121.65'
#lbIP='localhost'

lbPort=5670

credentials = pika.PlainCredentials('user1', 'password1')
parameters = pika.ConnectionParameters(host=lbIP, port=lbPort, virtual_host='vhost1', credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello4',durable=True)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(callback,
                      queue='hello4')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

#ACK - if consumer dies, messages will be re-delivered
# queue is declared as durable to prevent a situation of messages being lost when a broker dies
# but to make things working messages also need to be made durable at publisher side


#Note on message persistence

#Marking messages as persistent doesn't fully guarantee that a message won't be lost.
# Although it tells RabbitMQ to save the message to disk, there is still a short time
# window when RabbitMQ has accepted a message and hasn't saved it yet.
# Also, RabbitMQ doesn't do fsync(2) for every message -- it may be just saved to
# cache and not really written to the disk. The persistence guarantees aren't strong,
#  but it's more than enough for our simple task queue.
# If you need a stronger guarantee then you can use publisher confirms.

#after killing adaas: producer continued to send traffic but consumer did not reconnet successfuly

#raise exceptions.ChannelClosed(method.reply_code, method.reply_text)
#pika.exceptions.ChannelClosed: (404, "NOT_FOUND - home node 'rabbit@adaas' of durable queue 'hello4' in vhost 'vhost1' is down or inaccessible")

#This is because queues were not replicated, we need
#sudo rabbitmqctl set_policy -p "vhost1" ha-hello "^hello" '{"ha-mode":"all"}'
