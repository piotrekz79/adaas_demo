from kombu import Connection, Exchange, Queue, Consumer
import socket
import time
from datetime import datetime
rabbit_url = "amqp://user1:password1@134.221.121.65:5670/vhost1" #proxy
from kombu.log import get_logger
from kombu.utils.debug import setup_logging


logger=get_logger(__name__)
setup_logging(loglevel="DEBUG")


conn = Connection(rabbit_url, heartbeat=10)
exchange_adaas = Exchange("ex-adaas", type="fanout", durable=True)
queue_adaas_sec = Queue("q-adaas-sec2", exchange=exchange_adaas, durable=True)

def process_message(body, message):
    #print(str(datetime.now()) + " The body is {}".format(body))
    msg = str(datetime.now()) + " {}\n".format(body)
    print(msg)
    with open(out_file, "a+") as text_file:
        text_file.write(msg)
    message.ack()
    if "EOT" in body:
        exit()

consumer = Consumer(conn, queues=queue_adaas_sec, callbacks=[process_message], accept=["text/plain"])
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
            msg = str(datetime.now()) + " checking heartbeat\n"
            with open(out_file, "a+") as text_file:
                text_file.write(msg)

            print(msg)
            new_conn.heartbeat_check()

def consume_and_quit():
    new_conn = establish_connection()
    new_conn.drain_events(timeout=2)

def run():
    while True:
        time.sleep(5)
        print("slept..")
        try:
            #consume()
            consume_and_quit()
            #time.sleep(5)
        except conn.connection_errors:
            msg = str(datetime.now()) + " connection error\n"
            with open(out_file, "a+") as text_file:
                text_file.write(msg)
            print(msg)

out_file="/home/adaas/adaas_demo/q-sec" + str(datetime.now()).replace(" ","_")
#new_conn=establish_connection()
#run()
#consume_and_quit()
#conn.ensure_connection(max_retries=3)
#consumer.consume()
#new_conn.drain_events(timeout=2)
#new_conn.heartbeat_check()

#conn.close()
while True:
    print("sleeping..")
    time.sleep(5)
    print("slept..")
    with consumer:
        try:
            conn.drain_events(timeout=2)
        except socket.timeout:
            msg = str(datetime.now()) + " queue empty\n"
            with open(out_file, "a+") as text_file:
                text_file.write(msg)
            print(msg)

