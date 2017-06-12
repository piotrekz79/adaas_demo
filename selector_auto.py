#automatically reroutes traffic if primary publisher fails
import time
from pyrabbit.api import Client

pri_prod='prod1'
sec_prod='prod2'

cl = Client('localhost:15672', 'user1', 'password1')
cl.is_alive()


while True:
    disconnected1 = False
    disconnected2 = False

    print('checking producers presence...')
    time.sleep(3)

    channels=cl.get_channels()

    if not channels:
        disconnected1=True
        disconnected2=True
    elif not filter(lambda users: users['user'] == pri_prod, channels):
        disconnected1=True

    if disconnected1:
        print('producer ' + pri_prod + ' not connected, trying to switch to ' + sec_prod + '...')
        if not channels:
            disconnected2 = True
        elif not filter(lambda users: users['user'] == sec_prod, channels):
            disconnected2 = True

        if disconnected2:
            print('no producers available!')
        else:
            bindings=cl.get_queue_bindings('vhost1','q-adaas-top-1')

            print('producer ' + sec_prod + ' connected, switching to ' + sec_prod + '...')
            cl.create_binding(vhost='vhost1',exchange='ex-adaas-topic',queue="q-adaas-top-1",rt_key='top-2')

