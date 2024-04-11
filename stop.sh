podman stop --time=0 haproxy
podman stop --time=0 api1
podman stop --time=0 api2
podman rm haproxy
podman rm api1
podman rm api2
podman network rm apinetwork