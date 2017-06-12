#!/bin/bash

ssh adaas@adaas sudo rabbitmqctl start_app
ssh adaas@dane sudo rabbitmqctl start_app

ssh adaas@adaas sudo python /home/adaas/adaas_demo/kombu_consumer_ensure.py &
sleep 1
ssh adaas@dane sudo python /home/adaas/adaas_demo/kombu_producer_ensure.py &
sleep 10
ssh adaas@dane sudo rabbitmqctl stop_app
sleep 20
ssh adaas@dane sudo rabbitmqctl start_app
sleep 10
ssh adaas@adaas sudo rabbitmqctl stop_app
sleep 20
ssh adaas@adaas sudo rabbitmqctl start_app
sleep 10
ssh adaas@dane sudo rabbitmqctl stop_app
echo finished?

