if disconnected1:
    print('producer ' + pub1 + ' not connected, trying to switch to ' + pub2 + '...')
    if not channels:
        disconnected2 = True
    elif not filter(lambda users: users['user'] == pub2, channels):
        disconnected2 = True

    if disconnected2:
        print('no producers available!')
    else:
        bindings = cl.get_queue_bindings('vhost1', 'q-adaas-top-1')

        print('producer ' + pub2 + ' connected, switching to ' + pub2 + '...')
        cl.create_binding(vhost='vhost1', exchange='ex-adaas-topic', queue="q-adaas-top-1", rt_key='top-2')
