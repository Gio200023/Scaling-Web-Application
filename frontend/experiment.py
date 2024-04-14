import gevent
from locust.env import Environment

from locustfile import QuickstartUser
from locust.log import setup_logging
from stats_manager import StatsManager


def spawn_users(num_users):
    return env.runner.spawn_users({QuickstartUser.__name__: num_users})


if __name__ == "__main__":
    setup_logging("INFO")
    stats_manager = StatsManager()
    env = Environment(user_classes=[QuickstartUser])
    runner = env.create_local_runner()
    web_ui = env.create_web_ui('127.0.0.1', 8079)

    for i in range(60):
        gevent.spawn_later(i, stats_manager.fetch_stats)

    gevent.spawn_later(15, spawn_users, 1000)
    gevent.spawn_later(30, spawn_users, 1000)
    gevent.spawn_later(45, runner.quit)
    env.runner.spawn_users({QuickstartUser.__name__: 1000})
    env.runner.greenlet.join()
    web_ui.stop()
    print(stats_manager.current_sessions)
    print(stats_manager.response_times)
    print(stats_manager.containers)
    print(len(stats_manager.containers))
