from kombu import Connection, Exchange, Queue, Consumer
import socket
from datetime import datetime
rabbit_url = "amqp://user1:password1@134.221.121.65:5670/vhost1" #proxy
from kombu.log import get_logger
from kombu.utils.debug import setup_logging


logger=get_logger(__name__)
setup_logging(loglevel="DEBUG")


conn = Connection(rabbit_url, heartbeat=10)
exchange_adaas = Exchange("ex-adaas", type="fanout", durable=True)
queue_adaas_pri = Queue("q-adaas-pri", exchange=exchange_adaas, durable=True)

def process_message(body, message):
    #print(str(datetime.now()) + " The body is {}".format(body))
    msg = str(datetime.now()) + " {}\n".format(body)
    print(msg)
    with open(out_file, "a+") as text_file:
        text_file.write(msg)
    message.ack()
    if "EOT" in body:
        exit()

consumer = Consumer(conn, queues=queue_adaas_pri, callbacks=[process_message], accept=["text/plain"])
#consumer.consume()

def establish_connection():
    revived_connection = conn.clone()
    revived_connection.ensure_connection(max_retries=3)
    channel = revived_connection.channel()
    consumer.revive(channel)
    consumer.consume()
    return revived_connection

def consume():
    new_conn = establish_connection()
    while True:
        try:
            new_conn.drain_events(timeout=2)
        except socket.timeout:
            msg = str(datetime.now()) + " checking heartbeat\n"
            with open(out_file, "a+") as text_file:
                text_file.write(msg)

            print(msg)
            new_conn.heartbeat_check()
def run():
    while True:
        try:
            consume()
        except conn.connection_errors:
            msg = str(datetime.now()) + " connection error\n"
            with open(out_file, "a+") as text_file:
                text_file.write(msg)
            print(msg)

out_file="/home/adaas/adaas_demo/q-pri" + str(datetime.now()).replace(" ","_")
run()