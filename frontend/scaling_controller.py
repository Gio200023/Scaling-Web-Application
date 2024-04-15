import math
import time

import gevent
import numpy

from container_manager import ContainerManager
from stats_manager import StatsManager


class ScalingController:
    def __init__(self, stats_manager: StatsManager, container_manager: ContainerManager):
        self.stats_manager = stats_manager
        self.container_manager = container_manager
        self.determine_required_containers()

        try:
            while True:
                waited = 0
                while waited < 1:
                    self.stats_manager.fetch_stats()
                    time.sleep(0.1)
                    waited += 0.1

                self.determine_required_containers()
        finally:
            self.container_manager.scale_to(target_containers=0)

    def determine_required_containers(self):
        self.stats_manager.fetch_stats()

        if len(self.stats_manager.stats) == 0:
            self.container_manager.scale_to(target_containers=1)
            return

        avg_response_times = self.stats_manager.get_average_response_times(last_n=20)
        avg_response_time = numpy.average(avg_response_times)
        print("Average response time: " + str(avg_response_time) + "ms")
        num_containers = len(self.container_manager.list())
        if avg_response_time > 500:
            num_containers += math.ceil(avg_response_time / 500)

        if avg_response_time < 200:
            num_containers -= 1

        if avg_response_time < 150:
            num_containers -= 1

        if avg_response_time < 100:
            num_containers -= 1

        if avg_response_time == 0:
            num_containers = 1

        # self.container_manager.scale_to(target_containers=1)
        self.container_manager.scale_to(target_containers=max(num_containers, 1))


if __name__ == "__main__":
    stats_manager = StatsManager()
    container_manager = ContainerManager(stats_manager=stats_manager)
    scaling_controller = ScalingController(stats_manager=stats_manager, container_manager=container_manager)
