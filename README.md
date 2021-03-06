## plane-spotter-pi
The application receives SBS-1 messages by RTL-SDR. Clients interface is realised by Telegram Bot.
Infrastructure based on RaspberryPi and configured by ansible playbook-docker-compose.yml 
(https://github.com/metelitsaas/ansible-rpi-k8s)

### Services
All services set-up by docker-compose:
1. dump1090 - RTL-SDR decoder (https://github.com/malcolmrobb/dump1090).
2. sbs-receiver - parses received SBS-1 messages
3. web-server - saves messages to database and provides access
4. postgres - object-relational database for data storage
5. telegram-bot - client's interface

### Building notes
```
scp -r docker admin@192.168.0.18:/home/admin
scp -r apps admin@192.168.0.18:/home/admin
ssh admin@192.168.0.18 docker-compose -f docker/docker-compose.yml up -d
```

### Bot commands
#### 1. Get statistics
Command:
```
/statistics
```

Sample answer:
```
Statistics:
    All messages: 1639762
    Unique planes: 584
    Emergency messages: 0
```

#### 2. Get last message
Command:
```
/last_message
```

Sample answer:
```
Last message:
    Plane ID: 42495A
    Call sign: None
    UTC Timestamp: 2021-03-28 13:40:59
```
