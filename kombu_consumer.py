#https://medium.com/python-pandemonium/building-robust-rabbitmq-consumers-with-python-and-kombu-part-2-e9505f56e12e#.6u7zbhgqf

from kombu import Connection, Exchange, Queue #sudo pip install kombu
from kombu.mixins import ConsumerMixin
from kombu.log import get_logger
from kombu.utils.debug import setup_logging


logger=get_logger(__name__)

#rabbit_url = "amqp://134.221.121.65:5672/"
rabbit_url = "amqp://user1:password1@134.221.121.65:5670/vhost1" #proxy

class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues
    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message])]
    def on_message(self, body, message):
        print('Got message: {0}'.format(body))
        message.ack()
exchange = Exchange("ex2", type="topic", durable=True)
queues = [Queue("hello7", exchange, routing_key="hello7", durable=True)]
setup_logging(loglevel="DEBUG")

with Connection(rabbit_url, heartbeat=4) as conn:
        worker = Worker(conn, queues)
        worker.run()