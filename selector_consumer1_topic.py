from kombu import Connection, Exchange, Queue, Consumer
import socket
import time
from datetime import datetime
rabbit_url = "amqp://cons1:password1@134.221.121.65:5670/vhost1" #proxy
from kombu.log import get_logger
from kombu.utils.debug import setup_logging


logger=get_logger(__name__)
setup_logging(loglevel="DEBUG")


conn = Connection(rabbit_url, heartbeat=10)
exchange_adaas = Exchange("ex-adaas-topic", type="topic", durable=True)
#queue_adaas = Queue("q-adaas-top-1", exchange=exchange_adaas, durable=True, routing_key="top-1")
queue_adaas = Queue("q-adaas-top-1", exchange=exchange_adaas, durable=True)

def time_now():
    dt_now = datetime.now()
    epoch_now = (dt_now - datetime(1970, 1, 1)).total_seconds()
    msg = str("%.2f" % epoch_now) + "," + str(dt_now)
    return msg

def print_fc(msg,out_file):
    print(msg)
    with open(out_file, "a+") as text_file:
        text_file.write(msg)
    #print to file and console

def process_message(body, message):
    #print(str(datetime.now()) + " The body is {}".format(body))
    msg = time_now() + ",{}\n".format(body)
    print(msg)
    with open(out_file, "a+") as text_file:
        text_file.write(msg)
    message.ack()
    if "EOT" in body:
        exit()

consumer = Consumer(conn, queues=queue_adaas, callbacks=[process_message], accept=["text/plain"])

#consumer.consume()

def establish_connection():
    print("establish connection")
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
            msg = time_now() + ",checking heartbeat\n"
            with open(out_file, "a+") as text_file:
                text_file.write(msg)

            print(msg)
            new_conn.heartbeat_check()

def run():
    while True:
        try:
            consume()
        except conn.connection_errors:
            msg = time_now() + ",connection error\n"
            with open(out_file, "a+") as text_file:
                text_file.write(msg)
            print(msg)

#out_file="/home/adaas/adaas_demo/logs-selector/q-top-1-" + str(datetime.now()).replace(" ","_")
#out_file_log="/home/adaas/adaas_demo/logs-selector/log-q-top-1-" + str(datetime.now()).replace(" ","_")

out_fname="/home/adaas/adaas_demo/logs-selector/out_fname1.txt"
with open(out_fname, "r") as text_file:
    out_file=text_file.readline()

run()
