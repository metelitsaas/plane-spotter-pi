```
scp -r docker admin@192.168.0.18:/home/admin
scp -r apps admin@192.168.0.18:/home/admin

docker build \
--tag dump1090:1.0 \
--file docker/dump1090.dockerfile .

docker build \
--tag sbs-receiver:1.0 \
--file docker/sbs-receiver.dockerfile .

docker-compose -d -f docker/docker-compose.yml up
```