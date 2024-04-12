import math
import time

import numpy

from container_manager import ContainerManager
from stats_manager import StatsManager


class ScalingController:
    def __init__(self, stats_manager: StatsManager, container_manager: ContainerManager):
        self.stats_manager = stats_manager
        self.container_manager = container_manager

    def determine_required_containers(self):
        self.stats_manager.fetch_stats()

        if (len(self.stats_manager.response_times) == 0):
            self.container_manager.scale_to(target_containers=1)
            return

        average_response_time = numpy.average(self.stats_manager.response_times)
        percentile_response_time = numpy.percentile(self.stats_manager.response_times, 95)
        print("Average response time: " + str(average_response_time) + "ms")
        print("95th percentile response time: " + str(percentile_response_time) + "ms")
        num_containers = len(self.container_manager.list())
        if average_response_time > 250:
            extra_containers = math.ceil(average_response_time / 250)
            print("X", num_containers, extra_containers, num_containers + extra_containers)
            self.container_manager.scale_to(target_containers=max(num_containers + extra_containers, 1))
        elif percentile_response_time > 1000:
            extra_containers = math.ceil(percentile_response_time / 1000)
            print("Y", num_containers, extra_containers, num_containers + extra_containers)
            self.container_manager.scale_to(target_containers=max(num_containers + extra_containers, 1))
        elif average_response_time < 100 and percentile_response_time < 500:
            self.container_manager.scale_to(target_containers=max(num_containers - 1, 1))

    # current_sessions = self.stats_manager.current_sessions
    # print(current_sessions)
    # total_current_sessions = sum(current_sessions) / 100
    # print(total_current_sessions)
    # target_containers = math.ceil(total_current_sessions / 100)
    # target_containers = max(target_containers, 1)
    # self.container_manager.scale_to(target_containers=target_containers)


if __name__ == "__main__":
    stats_manager = StatsManager()
    container_manager = ContainerManager(stats_manager=stats_manager)
    scaling_controller = ScalingController(stats_manager=stats_manager, container_manager=container_manager)
    scaling_controller.determine_required_containers()

    try:
        while True:
            waited = 0
            stats_manager.reset()
            while waited < 5:
                stats_manager.fetch_stats()
                time.sleep(0.05)
                waited += 0.05

            scaling_controller.determine_required_containers()
    finally:
        scaling_controller.container_manager.scale_to(target_containers=0)
