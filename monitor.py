import requests
import csv
from io import StringIO

def fetch_haproxy_stats(url):
    """Fetch the stats from HAProxy stats URL, parse, filter and return relevant data."""
    response = requests.get(url)
    response.raise_for_status()  # Ensure we handle HTTP errors.
    f = StringIO(response.text)
    reader = csv.DictReader(f)
    filtered_stats = [row for row in reader if row['svname'].startswith('api')]
    return filtered_stats

def analyze_stats(stats):
    """Analyze stats and decide whether to scale up or down.
        if load is > 80 -> scale up
        if load is < 20 -> scale down    
    """
    scale_up_threshold = 80  # Threshold in percent to scale up
    scale_down_threshold = 20  # Threshold in percent to scale down
    scale_decision = 'No Scaling Needed'

    for stat in stats:
        current_load = int(stat['scur'])  # Current sessions
        max_load = int(stat['slim']) if stat['slim'] != '' else 100  # Safe default if no limit set
        
        # Calculate current load percentage
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
        while True:
            stats = fetch_haproxy_stats(haproxy_stats_url)
            decision = analyze_stats(stats)
            print(f"Decision: {decision}")
    except Exception as e:
        print(f"Failed to fetch or analyze HAProxy stats: {e}")
