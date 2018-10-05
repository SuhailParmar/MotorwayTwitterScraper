#!/bin/bash

# Run MQ in the background
sudo docker run -p 15672:15672 -p 5672:5672 rabbitmq:3.7-management &

# Create VHOST
curl -i -X PUT -u guest:guest http://localhost:15672/api/vhosts/motorway_vhost

# Create Exchange
curl -i -X PUT -u guest:guest http://localhost:15672/api/exchanges/new_vhost/MotorwayExchange

# Create M6 Queue
curl -i -X PUT -u guest:guest http://localhost:15672/api/queues/motorway_vhost/M6_Raw_Event


