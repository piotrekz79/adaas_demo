## adaas_demo

#haproxy
Edit the file
```
/etc/haproxy/haproxy.cfg
```

Add section

```
listen rabbit
	bind 134.221.121.65:5670
	balance roundrobin
        timeout client  3h
        timeout server  3h
	mode tcp
	option clitcpka
	server node-01 134.221.121.65:5672 check
	server node-02 134.221.121.63:5672 check
```
(we can also use frontend/backed blocks)

