#forwarder implementation - producer part; uses fanout exchange
from kombu import Connection, Producer, Queue, Exchange
import logging
import time
from datetime import datetime

rabbit_url = "amqp://prod1:password1@134.221.121.65:5670/vhost1" #proxy
#rabbit_url = "amqp://prod1:password1@134.221.121.63:5672/vhost1" #no proxy

conn = Connection(rabbit_url, transport_options={'confirm_publish': True})
producer = Producer(conn)

exchange_adaas = Exchange("ex-adaas", type="fanout", durable=True)
queue_adaas_pri = Queue("q-adaas-pri", exchange=exchange_adaas, durable=True)
queue_adaas_sec = Queue("q-adaas-sec2", exchange=exchange_adaas, durable=True)

def errback(exc, interval):
    logging.error('Error: %r', exc, exc_info=1)
    logging.info('Retry in %s seconds.', interval)

publish = conn.ensure(producer, producer.publish,
                          errback=errback, max_retries=3)
msg_body = 'START'
print str(datetime.now()) + " publishing " + msg_body
publish(msg_body, exchange=exchange_adaas, declare=[exchange_adaas, queue_adaas_pri, queue_adaas_sec])
#conn.release()

t=1
while t<101:
    publish = conn.ensure(producer, producer.publish,
                       errback=errback, max_retries=3)
    msg_body='hello ' + str(t)
    print str(datetime.now()) + " publishing " + msg_body
    publish(msg_body, exchange=exchange_adaas, declare=[exchange_adaas, queue_adaas_pri, queue_adaas_sec])
    t+=1
    time.sleep(1)

publish = conn.ensure(producer, producer.publish,
                       errback=errback, max_retries=3)
msg_body='EOT'
print str(datetime.now()) + " publishing " + msg_body
publish(msg_body, exchange=exchange_adaas, declare=[exchange_adaas, queue_adaas_pri, queue_adaas_sec])
conn.release()
