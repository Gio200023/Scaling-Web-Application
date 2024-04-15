import os
import shutil
import sys
import time

import gevent
from podman import PodmanClient
from podman.domain.containers import Container
from podman.domain.networks import Network
from podman.errors.exceptions import NotFound

from stats_manager import StatsManager


class ContainerManager:
    port = 8081
    client: PodmanClient = None
    network: Network = None
    network_ip: str = None
    haproxy_container: Container = None

    def __init__(self, stats_manager: StatsManager):
        self.stats_manager = stats_manager
        self.init_client()
        self.init_network()
        self.init_haproxy_container()

    def init_client(self):
        print("Initializing podman client...")
        self.client = PodmanClient(
            base_url="ssh://root@127.0.0.1:50654/run/podman/podman.sock",
            identity="/Users/jvdberg08/.local/share/containers/podman/machine/machine"
        )
        print("Done")

    def init_network(self):
        print("Initializing network...")
        try:
            self.network = self.client.networks.get(key='apinetwork')
        except NotFound:
            self.network = self.client.networks.create(name='apinetwork')
        self.network_ip = self.network.attrs.get('subnets')[0]['gateway']
        print("Done")

    def init_haproxy_container(self):
        print("Initializing haproxy configuration...")
        shutil.copyfile(src='./frontend/haproxy.cfg.temp', dst='./frontend/haproxy.cfg')
        print("Done")
        print("Initializing haproxy container...")
        try:
            self.haproxy_container = self.client.containers.get(key='haproxy')
        except NotFound:
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
        while not self.stats_manager.perform_health_check():
            time.sleep(0.05)
        print("Done")

    def get_image(self):
        return self.client.images.get(name="localhost/api:latest")

    def list(self):
        containers = self.client.containers.list()
        return [container for container in containers if container.name != 'haproxy']

    def create(self):
        self.port += 1
        container = self.client.containers.create(
            image=self.get_image(),
            volumes={'data': {'bind': '/server/data', 'mode': 'rw'}},
            networks={self.network.name: {self.network.name: self.network.name}},
            ports={'5001': str(self.port)},
            name="api" + str(self.port)
        )
        container.start()
        container.reload()
        file = open('./frontend/haproxy.cfg', 'a')
        file.write('  server ' + container.name + ' ' + self.network_ip + ':' + str(self.port) + ' check\n')

    def remove(self):
        self.port -= 1
        container = self.list()[-1]
        container.stop(ignore=True, timeout=0)
        container.remove(force=True, v=True)
        file = open('./frontend/haproxy.cfg', 'r')
        lines = file.readlines()[:-1]

        file = open('./frontend/haproxy.cfg', 'w')
        file.writelines(lines)

    def restart_haproxy_container(self):
        self.haproxy_container.restart(timeout=0)
        while not self.stats_manager.perform_health_check():
            time.sleep(0.05)

    def scale_to(self, target_containers: int):
        current_containers = len(self.list())
        if current_containers == target_containers:
            return

        print("Scaling from " + str(current_containers) + " to " + str(target_containers))

        events = []
        if current_containers > target_containers:
            containers_to_stop = current_containers - target_containers
            for _ in range(containers_to_stop):
                events.append(gevent.spawn(self.remove))

        else:
            containers_to_start = target_containers - current_containers
            for _ in range(containers_to_start):
                events.append(gevent.spawn(self.create))
        gevent.joinall(events)
        self.restart_haproxy_container()
        print("Scaled from " + str(current_containers) + " to " + str(target_containers))
