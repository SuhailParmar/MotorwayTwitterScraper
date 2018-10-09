#!/bin/bash

VHOST="motorway_vhost"
M6_QUEUE="M6_Raw_Event"
EXCHANGE="MotorwayExchange"
ROUTING_KEY="M6_Raw"

# Run MQ in the background
`sudo docker run --name rabbit-mq -h mq -p 15672:15672 -p 5672:5672 rabbitmq:3.7-management` &

echo "Waiting for Rabbit to be up..."
sleep 20 # ToDo use wait_for it

echo "Creating vhost: ${VHOST}"
curl -i -X PUT -u guest:guest http://localhost:15672/api/vhosts/${VHOST}

echo "Creating exchange: ${EXCHANGE}"
curl -i -X PUT -u guest:guest http://localhost:15672/api/exchanges/${VHOST}/${EXCHANGE}

echo "Creating Queue: ${M6_QUEUE}"
curl -i -X PUT -u guest:guest http://localhost:15672/api/queues/${VHOST}/${M6_QUEUE}

echo "Binding Queue: ${M6_QUEUE} to exchange: ${EXCHANGE} using routing key: ${ROUTING_KEY}"
curl -i -X POST -u guest:guest \
  --data '{"routing_key":"M6_Raw","arguments":{}}'\
    http://localhost:15672/api/bindings/${VHOST}/e/${EXCHANGE}/q/${M6_QUEUE}
