import requests
import csv
from io import StringIO
from requests.exceptions import ConnectionError


class StatsManager:
    url = 'http://localhost:8081/;csv'
    current_sessions = []
    response_times = []
    containers = []

    def perform_health_check(self):
        try:
            requests.get(url=self.url)
            return True
        except ConnectionError as e:
            print(e)
            return False

    def reset(self):
        self.current_sessions = []
        self.response_times = []

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
        self.containers.append(len(filtered_stats))

        for stat in filtered_stats:
            # if index >= len(self.current_sessions):
            #     self.current_sessions.append(int(stat['scur']))
            # else:
            #     self.current_sessions[index] += int(stat['scur'])
            self.current_sessions.append(int(stat['scur']))
            self.response_times.append(int(stat['ttime']))
            # if index >= len(self.response_times):
            #     self.response_times.append(int(stat['ttime']))
            # else:
            #     self.response_times[index] += int(stat['ttime'])
