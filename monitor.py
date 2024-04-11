import requests
import csv
from io import StringIO

def fetch_haproxy_stats(url):
    """Fetch the stats from HAProxy stats URL and return as text."""
    response = requests.get(url)
    response.raise_for_status() 
    return response.text

def parse_stats(csv_data):
    """Parse CSV data into a list of dictionaries, one per stats entry."""
    f = StringIO(csv_data)
    reader = csv.DictReader(f, delimiter=',')
    return list(reader)

def analyze_stats(stats):
    """Analyze stats and decide whether to scale up or down.
        if load is > 80 -> scale up
        if load is < 20 -> scale down
    """
    scale_up_threshold = 80  
    scale_down_threshold = 20
    scale_decision = 'No Scaling Needed'

    for stat in stats:
        if stat['svname'] != 'BACKEND' and stat['svname'] != 'FRONTEND':
            current_load = int(stat['scur'])
            max_load = int(stat['slim']) if stat['slim'] != '' else 100  # Safe default if no limit set

            load_percentage = (current_load / max_load) * 100 if max_load > 0 else 0

            if load_percentage > scale_up_threshold:
                scale_decision = 'Scale Up'
            elif load_percentage < scale_down_threshold:
                scale_decision = 'Scale Down'

            # Print current load information
            print(f"Server: {stat['svname']}, Current Load: {current_load}, Max Load: {max_load}, Load %: {load_percentage}%")

    return scale_decision

if __name__ == "__main__":
    haproxy_stats_url = 'http://localhost:8081/;csv'
    try:
        data = fetch_haproxy_stats(haproxy_stats_url)
        stats = parse_stats(data)
        decision = analyze_stats(stats)
        print(f"Decision: {decision}")
    except Exception as e:
        print(f"Failed to fetch or analyze HAProxy stats: {e}")
