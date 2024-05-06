import gevent
from locust.env import Environment

from locustfile import QuickstartUser
from stats_manager import StatsManager
import matplotlib.pyplot as plt


def spawn_users(num_users):
    return env.runner.spawn_users({QuickstartUser.__name__: num_users})


def stop_users(num_users):
    return env.runner.stop_users({QuickstartUser.__name__: num_users})


if __name__ == "__main__":

    stats_manager = StatsManager()
    env = Environment(user_classes=[QuickstartUser])
    runner = env.create_local_runner()
    web_ui = env.create_web_ui('127.0.0.1', 8079)

    for i in range(180):
        gevent.spawn_later(i, stats_manager.fetch_stats)

    gevent.spawn_later(5, spawn_users, 25)
    gevent.spawn_later(20, spawn_users, 750)
    gevent.spawn_later(40, stop_users, 500)
    gevent.spawn_later(60, spawn_users, 1000)
    gevent.spawn_later(80, spawn_users, 50)
    gevent.spawn_later(100, stop_users, 150)
    gevent.spawn_later(140, stop_users, 500)
    gevent.spawn_later(160, stop_users, 400)
    gevent.spawn_later(180, runner.quit)
    env.runner.spawn_users({QuickstartUser.__name__: 25})
    env.runner.greenlet.join()
    web_ui.stop()

    current_session = stats_manager.get_current_sessions()
    response_times = stats_manager.get_average_response_times(last_n=None)
    request_rates = stats_manager.request_rates
    container = [len(x) for x in stats_manager.stats]

    plt.figure(figsize=(14, 7))

    # Current Sessions Plot
    plt.subplot(3, 1, 1)  # 3 rows, 1 column, 1st subplot
    plt.plot(current_session, label='Current Sessions', color='blue')
    plt.title('Current Sessions Over Time')
    plt.xlabel('Steps')
    plt.ylabel('Number of Sessions')

    # Request rate Plot
    # plt.subplot(3, 1, 1)
    # plt.plot(request_rates, label='Requests Per Second', color='green')
    # plt.title('RPS Over Time')
    # plt.xlabel('Steps')
    # plt.ylabel('Requests Per Second')

    # Response Times Plot
    plt.subplot(3, 1, 2)
    plt.plot(response_times, label='Response Times', color='red')
    plt.title('Response Times Over Time')
    plt.xlabel('Steps')
    plt.ylabel('Response Time (ms)')

    # Containers Plot
    plt.subplot(3, 1, 3)
    plt.plot(container, label='Number of Containers', color='blue')
    plt.title('Number of Containers Over Time')
    plt.xlabel('Steps')
    plt.ylabel('Number of Containers')

    plt.tight_layout()
    plt.savefig("experiments.png")
    print(stats_manager.downtime)
