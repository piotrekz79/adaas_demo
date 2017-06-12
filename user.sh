sudo rabbitmqctl add_user user1 password1
sudo rabbitmqctl add_vhost vhost1
sudo rabbitmqctl set_permissions -p vhost1 user1 ".*" ".*" ".*"


