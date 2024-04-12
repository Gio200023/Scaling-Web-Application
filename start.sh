podman network create apinetwork
podman create \
  --network apinetwork \
  --name haproxy \
  -p 80:8080 \
  -p 8081:8081 \
  -v ./haproxy/haproxy.cfg.temp:/usr/local/etc/haproxy/haproxy.cfg \
  haproxy:2.9.7-alpine3.19
podman create -v ./data:/server/data --network apinetwork --name api1 -p 8082:5001 api
podman create -v ./data:/server/data --network apinetwork --name api2 -p 8083:5001 api
podman start haproxy
podman start api1
podman start api2