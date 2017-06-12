#!/bin/bash

#ssh adaas@adaas sudo rabbitmqctl stop_app
#ssh adaas@dane sudo rabbitmqctl stop_app
#sleep 2
ssh adaas@adaas sudo rabbitmqctl start_app
sleep 5
ssh adaas@adaas sudo python /home/adaas/adaas_demo/kombu_consumer_ensure.py &
sleep 1
ssh adaas@dane sudo rabbitmqctl start_app
sleep 5
ssh adaas@dane sudo python /home/adaas/adaas_demo/kombu_producer_ensure.py &

ssh adaas@dane 'sudo netstat -pan | grep 5672'
 
#for i in `seq 5`; do
sleep 10
ssh adaas@dane sudo rabbitmqctl stop_app
sleep 15
ssh adaas@dane sudo rabbitmqctl start_app
sleep 10
ssh adaas@adaas sudo rabbitmqctl stop_app
sleep 15
ssh adaas@adaas sudo rabbitmqctl start_app
sleep 15
ssh adaas@dane sudo rabbitmqctl stop_app
sleep 5
ssh adaas@adaas sudo rabbitmqctl stop_app

#done
echo finished?

