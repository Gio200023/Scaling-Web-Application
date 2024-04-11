import time

from podman import PodmanClient


class ContainerManager:

    def __init__(self):
        self.client = PodmanClient(
            base_url="ssh://core@127.0.0.1:50847/run/user/501/podman/podman.sock",
            identity="/Users/jvdberg08/.local/share/containers/podman/machine/machine"
        )

    def get_image(self):
        return self.client.images.get(name="objst:latest")

    def list(self):
        return self.client.containers.list()

    def create(self):
        return self.client.containers.create(
            image=self.get_image(),
            volumes={'data': {'bind': '/server/data', 'mode': 'rw'}}
        )


if __name__ == "__main__":
    container_manager = ContainerManager()
    print(container_manager.list())
    containers = [
        container_manager.create(),
        container_manager.create(),
        container_manager.create(),
        container_manager.create()
    ]
    print(containers)

    for container in containers:
        container.start()
        container.reload()
        print(container.status)
        print(container.attrs['NetworkSettings']['Networks']['podman']['IPAddress'])

    for container in containers:
        container.remove(force=True)
