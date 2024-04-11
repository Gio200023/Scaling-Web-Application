#!/usr/bin/env bash

# build ha proxy
podman build -t haproxy .

# Run haproxy-server in podman network from haproxy image
podman run --replace --name haproxy-server -p 80:80 -p 8084:8084 --network webappnet -d haproxy