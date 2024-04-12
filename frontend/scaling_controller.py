import math
import time

from container_manager import ContainerManager
from stats_manager import StatsManager


class ScalingController:
    def __init__(self, stats_manager: StatsManager, container_manager: ContainerManager):
        self.stats_manager = stats_manager
        self.container_manager = container_manager

    def determine_required_containers(self):
        self.stats_manager.fetch_stats()
        current_sessions = self.stats_manager.current_sessions
        print(current_sessions)
        total_current_sessions = sum(current_sessions) / 100
        print(total_current_sessions)
        target_containers = math.ceil(total_current_sessions / 100)
        target_containers = max(target_containers, 1)
        self.container_manager.scale_to(target_containers=target_containers)


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
