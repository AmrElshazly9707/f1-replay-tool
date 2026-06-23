import requests
import os
import requests_cache
import pandas as pd

# Caches responses locally to speed up subsequent executions.
# Expires after a day
requests_cache.install_cache('openf1_cache', expire_after = 86400)

# Clears up stored data in the cache to prevent lag
def cleanup_cache(max_bytes = 100_000_000, force = False):
    # Clear the requests_cache DB if it exceeds (max_bytes) or if (force) is True.
    cache_file = 'openf1_cache.sqlite'
    if os.path.exists(cache_file) and (force or os.path.getsize(cache_file) > max_bytes):
        requests_cache.clear()
        os.remove(cache_file)

# Establishes a persistent connection pool to reduce network latency.
api_session = requests.Session()

# Base url for accessing OpenF1
BASE_URL = "https://api.openf1.org/v1"

# Fetches data for a chosen year
def fetch_year_data(chosen_year : int):

    payload = {'year' : chosen_year}

    sessions_data = api_session.get(f"{BASE_URL}/sessions", params = payload).json()
    meetings_data = api_session.get(f"{BASE_URL}/meetings", params = payload).json()

    return {
        "sessions" : sessions_data,
        "meetings" : meetings_data
    }

