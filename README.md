## plane-spotter-pi
The application receives SBS-1 messages by RTL-SDR. 
Infrastructure based on RaspberryPi and configured by ansible playbook-docker-compose.yml 
(https://github.com/metelitsaas/ansible-rpi-k8s)

### Services
All services set-up by docker-compose:
1. dump1090 - RTL-SDR decoder (https://github.com/malcolmrobb/dump1090).
2. sbs-receiver - parses received SBS-1 messages

### Building notes
```
scp -r docker admin@192.168.0.18:/home/admin
scp -r apps admin@192.168.0.18:/home/admin

docker-compose -f docker/docker-compose.yml up -d
```