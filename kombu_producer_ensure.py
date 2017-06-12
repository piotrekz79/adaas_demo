from kombu import Connection, Producer, Queue, Exchange
import logging
import time
from datetime import datetime

rabbit_url = "amqp://user1:password1@134.221.121.65:5670/vhost1" #proxy
#rabbit_url = "amqp://user1:password1@134.221.121.63:5672/vhost1" #no proxy

conn = Connection(rabbit_url, transport_options={'confirm_publish': True})
producer = Producer(conn)

exchange = Exchange("ex2", type="topic", durable=True)
queues = Queue("hello7", exchange, routing_key="hello7", durable=True)

def errback(exc, interval):
    logging.error('Error: %r', exc, exc_info=1)
    logging.info('Retry in %s seconds.', interval)

publish = conn.ensure(producer, producer.publish,
                          errback=errback, max_retries=3)
msg_body = 'START'
print str(datetime.now()) + " publishing " + msg_body
publish(msg_body, routing_key='hello7', exchange=queues.exchange, declare=[queues])
conn.release()

t=1
while t<101:
    publish = conn.ensure(producer, producer.publish,
                       errback=errback, max_retries=3)
    msg_body='hello ' + str(t)
    print str(datetime.now()) + " publishing " + msg_body
    publish(msg_body, routing_key='hello7', exchange = queues.exchange, declare=[queues])
    t+=1
    time.sleep(1)

publish = conn.ensure(producer, producer.publish,
                       errback=errback, max_retries=3)
msg_body='EOT'
print str(datetime.now()) + " publishing " + msg_body
publish(msg_body, routing_key='hello7', exchange = queues.exchange, declare=[queues])
conn.release()
