#automatically reroutes traffic if primary publisher fails
import time
from pyrabbit.api import Client
from pyrabbit.api import http
pub1='prod1'
pub2='prod2'
a_vhost='vhost1'
a_exchange='ex-adaas-topic'
a_Q1='q-adaas-top-1'
a_Q2='q-adaas-top-2'
a_key1='top-1'
a_key2='top-2'
a_delay=3


def override():
#TODO
    return False

def failover(cl):
    print('failover mode')

    qbindings=cl.get_queue_bindings(vhost=a_vhost, qname=a_Q1)
    if not qbindings:
        print('error: queue ' + a_Q1 + ' has no bindings at all')
        #exit(1)

    elif not filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q1) & (qb['routing_key']==a_key2), qbindings):
        print('creating binding ' + pub2 + ' to ' + a_Q1)
        cl.create_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key2)
        if filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q1) & (qb['routing_key']==a_key1), qbindings):
            print('removing binding ' + pub1 + ' to ' + a_Q1)
            cl.delete_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key1)

    qbindings = cl.get_queue_bindings(vhost=a_vhost, qname=a_Q2)
    if not qbindings:
            print('error: queue ' + a_Q2 + ' has no bindings at all')
            #exit(1)

    elif filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q2) & (qb['routing_key']==a_key2), qbindings):
        print('removing binding ' + pub2 + ' to ' + a_Q2)
        cl.delete_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q2, rt_key=a_key2)


def normal(cl):
    print('normal mode')

    qbindings=cl.get_queue_bindings(vhost=a_vhost, qname=a_Q1)
    if not qbindings:
        print('error: queue ' + a_Q1 + ' has no bindings at all')
        #exit(1)

    elif not filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q1) & (qb['routing_key']==a_key1), qbindings):
        print('creating binding ' + pub1 + ' to ' + a_Q1)
        cl.create_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key1)
        if filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q1) & (qb['routing_key']==a_key2), qbindings):
            print('removing binding ' + pub2 + ' to ' + a_Q1)
            cl.delete_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key2)


    qbindings = cl.get_queue_bindings(vhost=a_vhost, qname=a_Q2)
    if not qbindings:
        print('error: queue ' + a_Q2 + ' has no bindings at all')
        #exit(1)

    elif not filter(lambda qb: (qb['source'] == a_exchange) & (qb['destination']==a_Q2) & (qb['routing_key']==a_key2), qbindings):
        print('creating binding ' + pub2 + ' to ' + a_Q2)
        cl.create_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q2, rt_key=a_key2)





def master_alarm():
    print('master alarm ! All publishers disconnected')

cl = Client('localhost:15672', 'user1', 'password1')

if cl.is_alive():
    cl.create_queue(vhost=a_vhost, name=a_Q1, durable=True)
    cl.create_queue(vhost=a_vhost, name=a_Q2, durable=True)

    try:
        cl.delete_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key2)
    except http.HTTPError:
        print("no binding " + pub2 + " to " + a_Q1)

    try:
        cl.delete_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q2, rt_key=a_key1)
    except http.HTTPError:
        print("no binding " + pub1 + " to " + a_Q2)


    cl.create_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q1, rt_key=a_key1)
    cl.create_binding(vhost=a_vhost, exchange=a_exchange, queue=a_Q2, rt_key=a_key2)

while True:
    pub1_conn = True
    pub2_conn = True

    print('checking publishers presence...')
    time.sleep(a_delay)

    channels=cl.get_channels()


    if not channels:
        pub1_conn = False
        pub2_conn = False
    else: #we can iterate only if channels are not empty
        if not filter(lambda users: users['user'] == pub1, channels):
            pub1_conn = False
        if not filter(lambda users: users['user'] == pub2, channels):
            pub2_conn = False

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


