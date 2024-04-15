from typing import Union, Optional

import numpy
import requests
import csv
from io import StringIO
from requests.exceptions import ConnectionError


class StatsManager:
    url = 'http://localhost:8081/;csv'
    stats = []

    def perform_health_check(self):
        try:
            requests.get(url=self.url)
            return True
        except ConnectionError as e:
            return False

    def get_current_sessions(self):
        current_sessions = []
        for stat in self.stats:
            sessions = [x['sessions'] for x in stat]
            current_sessions.append(sum(sessions))
        return current_sessions

    def get_average_response_times(self, last_n: Optional[int] = None):
        if last_n is None:
            stats = self.stats
        else:
            stats = self.stats[-last_n:]
        response_times = []
        for stat in stats:
            r_times = []
            for container_stat in stat:
                r_times.append(container_stat['response_time'])
            response_times.append(numpy.average(r_times))
        return response_times

    def get_response_times(self, last_n: Optional[int] = None):
        if last_n is None:
            stats = self.stats
        else:
            stats = self.stats[-last_n:]
        response_times = []
        for stat in stats:
            for container_stat in stat:
                response_times.append(container_stat['response_time'])
        return response_times

    def fetch_stats(self):
        """Fetch the stats from HAProxy stats URL, parse, filter and return relevant data."""
        retry = True
        while retry:
            try:
                response = requests.get(url=self.url)
                retry = False
            except ConnectionError:
                pass
        response.raise_for_status()
        file = StringIO(response.text)
        reader = csv.DictReader(file)
        filtered_stats = [row for row in reader if row['svname'].startswith('api')]
        if len(filtered_stats) == 0:
            return

        stats = []
        for stat in filtered_stats:
            stats.append({
                "sessions": int(stat['scur']),
                "response_time": int(stat['ttime'])
            })
        self.stats.append(stats)
