import os
import shutil
import sys

from podman import PodmanClient
from podman.domain.containers import Container
from podman.errors.exceptions import NotFound


class ContainerManager:
    port = 8081

    def __init__(self):
        print("Initializing haproxy configuration...")
        shutil.copyfile(src='./haproxy.cfg.temp', dst='./haproxy.cfg')
        print("Done")
        print("Initializing podman client...")
        self.client = PodmanClient(
            base_url="ssh://root@127.0.0.1:50654/run/podman/podman.sock",
            identity="/Users/jvdberg08/.local/share/containers/podman/machine/machine"
        )
        print("Done")
        print("Initializing network...")
        self.network = self.client.networks.create(name='apinetwork')
        self.network_ip = self.network.attrs.get('subnets')[0]['gateway']
        print("Done")
        print("Creating haproxy container...")
        self.haproxy_container = self.client.containers.create(
            image=self.client.images.pull(
                repository="docker.io/library/haproxy",
                tag="2.9.7-alpine3.19"
            ),
            mounts=[{
                'type': 'bind',
                'source': os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), './haproxy.cfg'),
                'target': '/usr/local/etc/haproxy/haproxy.cfg',
                'read_only': True
            }],
            ports={'8080': '80', '8081': '8081'},
            name="haproxy",
            networks={self.network.name: {self.network.name: self.network.name}},
        )
        self.haproxy_container.start()
        self.haproxy_container.reload()
        print("Done")

    def get_image(self):
        return self.client.images.get(name="localhost/api:latest")

    def list(self):
        return self.client.containers.list()

    def create(self):
        self.port += 1
        return self.client.containers.create(
            image=self.get_image(),
            volumes={'data': {'bind': '/server/data', 'mode': 'rw'}},
            networks={self.network.name: {self.network.name: self.network.name}},
            ports={'5001': str(self.port)},
            name="api" + str(self.port)
        )

    def add_to_haproxy_cfg(self, container: Container, port: str):
        file = open('./haproxy.cfg', 'a')
        file.write('  server ' + container.name + ' ' + self.network_ip + ':' + port + ' check\n')
        self.haproxy_container.restart()


if __name__ == "__main__":
    container_manager = None
    try:
        container_manager = ContainerManager()

        container = container_manager.create()
        container.start()
        container.reload()
        container_manager.add_to_haproxy_cfg(container=container, port=str(container_manager.port))

        container = container_manager.create()
        container.start()
        container.reload()
        container_manager.add_to_haproxy_cfg(container=container, port=str(container_manager.port))

        container = container_manager.create()
        container.start()
        container.reload()
        container_manager.add_to_haproxy_cfg(container=container, port=str(container_manager.port))

        while True:
            pass
    finally:
        print("Exiting... (may take a while, 10s for every container)")
        if container_manager is not None:
            for container in container_manager.network.containers:
                container.remove(force=True)
            container_manager.network.remove(force=True)
