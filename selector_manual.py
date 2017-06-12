#automatically reroutes traffic if primary publisher fails
import time
from pyrabbit.api import Client
from pyrabbit.api import http
from datetime import datetime

pub1='prod1'
pub2='prod2'
cons1='cons1'
cons2='cons2'
a_vhost='vhost1'
a_exchange='ex-adaas-topic'
a_Q1='q-adaas-top-1'
a_Q2='q-adaas-top-2'
a_key1='top-1'
a_key2='top-2'
a_delay=3


def time_now():
    dt_now = datetime.now()
    epoch_now = (dt_now - datetime(1970, 1, 1)).total_seconds()
    msg = str("%.2f" % epoch_now) + "," + str(dt_now)
    return msg


def print_fc_now(out_file1,out_file2,msg):
    msg = time_now() + "," + msg
    print(msg)
    with open(out_file1, "a+") as text_file:
        text_file.write(msg)

    with open(out_file2, "a+") as text_file:
        text_file.write(msg)


def override():
#TODO
    return False

def failover(cl):
    print_fc_now(out_file1,out_file2,'failover mode')

    qbindings=cl.get_queue_bindings(vhost=a_vhost, qname=a_Q1)
    if not qbindings:
        print_fc_now(out_file1,out_file2,'error: queue ' + a_Q1 + ' has no bindings at all')
        #exit(1)

    elif not filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q1) & (qb['routing_key']==a_key2), qbindings):
        print_fc_now(out_file1,out_file2,'creating binding ' + pub2 + ' to ' + a_Q1)
        cl.create_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key2)
        if filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q1) & (qb['routing_key']==a_key1), qbindings):
            print_fc_now(out_file1,out_file2,'removing binding ' + pub1 + ' to ' + a_Q1)
            cl.delete_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key1)

    qbindings = cl.get_queue_bindings(vhost=a_vhost, qname=a_Q2)
    if not qbindings:
            print_fc_now(out_file1,out_file2,'error: queue ' + a_Q2 + ' has no bindings at all')
            #exit(1)

    elif filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q2) & (qb['routing_key']==a_key2), qbindings):
        print_fc_now(out_file1,out_file2,'removing binding ' + pub2 + ' to ' + a_Q2)
        cl.delete_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q2, rt_key=a_key2)

def failover_for_manual(cl):
    print_fc_now(out_file1,out_file2,'failover for manual mode')

    qbindings=cl.get_queue_bindings(vhost=a_vhost, qname=a_Q2)
    if not qbindings:
        print_fc_now(out_file1,out_file2,'error: queue ' + a_Q2 + ' has no bindings at all')
        #exit(1)

    elif not filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q2) & (qb['routing_key']==a_key1), qbindings):
        print_fc_now(out_file1,out_file2,'creating binding ' + pub1 + ' to ' + a_Q2)
        cl.create_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q2, rt_key=a_key1)
        if filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q2) & (qb['routing_key']==a_key2), qbindings):
            print_fc_now(out_file1,out_file2,'removing binding ' + pub2 + ' to ' + a_Q2)
            cl.delete_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q2, rt_key=a_key2)

    qbindings = cl.get_queue_bindings(vhost=a_vhost, qname=a_Q1)
    if not qbindings:
        print_fc_now(out_file1,out_file2,'error: queue ' + a_Q1 + ' has no bindings at all')
        #exit(1)

    elif filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q1) & (qb['routing_key']==a_key1), qbindings):
        print_fc_now(out_file1,out_file2,'removing binding ' + pub1 + ' to ' + a_Q1)
        cl.delete_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key1)

def normal(cl):
    print_fc_now(out_file1,out_file2,'normal mode')

    qbindings=cl.get_queue_bindings(vhost=a_vhost, qname=a_Q1)
    if not qbindings:
        print_fc_now(out_file1,out_file2,'error: queue ' + a_Q1 + ' has no bindings at all')
        #exit(1)

    elif not filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q1) & (qb['routing_key']==a_key1), qbindings):
        print_fc_now(out_file1,out_file2,'creating binding ' + pub1 + ' to ' + a_Q1)
        cl.create_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key1)
        if filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q1) & (qb['routing_key']==a_key2), qbindings):
            print_fc_now(out_file1,out_file2,'removing binding ' + pub2 + ' to ' + a_Q1)
            cl.delete_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key2)


    qbindings = cl.get_queue_bindings(vhost=a_vhost, qname=a_Q2)
    if not qbindings:
        print_fc_now(out_file1,out_file2,'error: queue ' + a_Q2 + ' has no bindings at all')
        #exit(1)

    elif not filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q2) & (qb['routing_key']==a_key2), qbindings):
        print_fc_now(out_file1,out_file2,'creating binding ' + pub2 + ' to ' + a_Q2)
        cl.create_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q2, rt_key=a_key2)





def master_alarm():
    print_fc_now(out_file1,out_file2,'master alarm ! All publishers disconnected')

cl = Client('localhost:15672', 'user1', 'password1')

if cl.is_alive():
    cl.create_queue(vhost=a_vhost, name=a_Q1, durable=True)
    cl.create_queue(vhost=a_vhost, name=a_Q2, durable=True)

    try:
        cl.delete_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key2)
    except http.HTTPError:
        print_fc_now(out_file1,out_file2,"no binding " + pub2 + " to " + a_Q1)

    try:
        cl.delete_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q2, rt_key=a_key1)
    except http.HTTPError:
        print_fc_now(out_file1,out_file2,"no binding " + pub1 + " to " + a_Q2)


    cl.create_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key1)
    cl.create_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q2, rt_key=a_key2)

    dt_now=str(datetime.now()).replace(" ","_")
    out_file1="/home/adaas/adaas_demo/logs-selector/q-top-1-" + dt_now
    out_file2="/home/adaas/adaas_demo/logs-selector/q-top-2-" + dt_now
    out_fname1="/home/adaas/adaas_demo/logs-selector/out_fname1.txt"
    out_fname2="/home/adaas/adaas_demo/logs-selector/out_fname2.txt"

    with open(out_fname1, "w+") as text_file:
        text_file.write(out_file1)

    with open(out_fname2, "w+") as text_file:
        text_file.write(out_file2)



while True:
    pub1_conn = True
    pub2_conn = True
    cons1_conn = True
    cons2_conn = True

    print_fc_now(out_file1,out_file2,'checking publishers and consumers presence...')
    time.sleep(a_delay)

    channels=cl.get_channels()


    if not channels:
        pub1_conn = False
        pub2_conn = False
        cons1_conn = False
        cons2_conn = False

    else: #we can iterate only if channels are not empty
        if not filter(lambda users: users['user'] == pub1, channels):
            pub1_conn = False
        if not filter(lambda users: users['user'] == pub2, channels):
            pub2_conn = False
        if not filter(lambda users: users['user'] == cons1, channels):
            cons1_conn = False
        if not filter(lambda users: users['user'] == cons2, channels):
            cons2_conn = False

    if cons1_conn:
        if pub1_conn:
            if override():
                failover(cl=cl)
            else:
                normal(cl=cl)
        #pub1 not connected, try to failover
        elif pub2_conn:
            failover(cl=cl)
        else:
            master_alarm()
    elif cons2_conn: #even if both are connected, cons1 has priority
        if pub2_conn:
            normal(cl=cl)
        elif pub1_conn:
            failover_for_manual(cl=cl)
        else:
            master_alarm()
    else:
        print_fc_now(out_file1,out_file2,'waiting for consumers...')


