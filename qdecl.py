#!/usr/bin/env python
import pika

msgbody='Hello3 World!'

lbIP='134.221.121.65'
#lbIP='localhost'

lbPort=5670

credentials = pika.PlainCredentials('user1', 'password1')
parameters = pika.ConnectionParameters(host=lbIP, port=lbPort, virtual_host='vhost1', credentials=credentials)

for i in range(1,5):
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue='hello200'+str(i))
    connection.close()


#master (home node) w.r.t. queue is the node on which queue was first time declared (Q master), NOT the master of the cluster
#If we have a Round robin LB and close connection in a loop queues are declared in a round robin fashion on the cluster nodes
#if we keep only queue_declare in a loop, all queues will end up on the same node

#https://www.erlang-solutions.com/blog/take-control-of-your-rabbitmq-queues.html
#Currently, there are three queue master location strategies available;
#Min-Masters: Selects the master node as the one with the least running master queues. Configured as min-masters.
#Client-local: Like previous default node selection policy, this strategy selects the queue master node as the local node on which the queue is being declared. Configured as client-local.
#Random: Selects the queue master node based on random selection. Configured as random.
