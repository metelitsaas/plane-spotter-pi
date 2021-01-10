## plane-spotter-pi
The application receives SBS-1 messages by RTL-SDR and sends them to RabbitMQ broker. 
Infrastructure based on RaspberryPi and configurated by ansible playbook-docker-compose.yml (https://github.com/metelitsaas/ansible-rpi-k8s)

### Services
All services set-up by docker-compose:
1. dump1090 - RTL-SDR decoder (https://github.com/malcolmrobb/dump1090).
2. sbs-receiver - parses received SBS-1 messages, transforms them and sends to RabbitMQ broker.
3. rabbitmq - RabbitMQ one-node broker.

### Building notes
```
scp -r docker admin@192.168.0.18:/home/admin
scp -r apps admin@192.168.0.18:/home/admin

docker build \
--tag dump1090:1.0 \
--file docker/dump1090.dockerfile .

docker build \
--tag sbs-receiver:1.0 \
--file docker/sbs-receiver.dockerfile .

docker-compose -f docker/docker-compose.yml up -d
```