import requests
import os
import requests_cache
import pandas as pd
from typing import Literal
from datetime import datetime
import zoneinfo

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

class F1DataManager:

    # Base url for accessing OpenF1
    BASE_URL = "https://api.openf1.org/v1"

    # List that contains the available years from 2023 to the present
    available_years = list(range(2023, datetime.today().year + 1))

    # Limits session types to the three available types
    AllowedSessionTypes = Literal["Practice" , "Qualifying" , "Race"]

    # All available timezones to choose from
    all_timezones = sorted(zoneinfo.available_timezones())

    def __init__ (self):

        # Establishes a persistent connection pool to reduce network latency.
        self.api_session = requests.Session()

        self.practice = {}
        self.qualifying = {}
        self.race = {}
        self.meetings = {}
        self.circuits = []

    # Fetches data for a chosen year
    def fetch_year_data(self, chosen_year : int):

        payload = {'year' : chosen_year}

        sessions_data = self.api_session.get(f"{self.BASE_URL}/sessions", params = payload).json()
        meetings_data = self.api_session.get(f"{self.BASE_URL}/meetings", params = payload).json()

        # Grouping each session_type in its own dict of dicts

        self.practice = {int(p['meeting_key']) : p 
                        for p in sessions_data 
                        if p.get('session_type') == 'Practice' and 'circuit_short_name' in p}

        self.qualifying = {int(q['meeting_key']) : q
                        for q in sessions_data 
                        if q.get('session_type') == 'Qualifying' and 'circuit_short_name' in q}

        self.race = {int(r['meeting_key']) : r
                    for r in sessions_data 
                    if r.get('session_type') == 'Race' and 'circuit_short_name' in r}

        # Dict of dicts of meetings accessed by meeting_key
        self.meetings = {int(key['meeting_key']) : key for key in meetings_data if 'meeting_key' in key}

        unique_circuits = {}
        for session in sessions_data:
            meeting_key = session.get('meeting_key')
            circuit_name = session.get('circuit_short_name')
            if meeting_key is not None and circuit_name:
                unique_circuits[int(meeting_key)] = circuit_name

        # List of the names of all circuits
        self.circuits = sorted(list(unique_circuits.items()), key = lambda x : x[1])

    # Fetches a session and raises a KeyError exception if there is no such session
    def get_session_safely(self, meeting_key, session_type):
        try:
            if session_type == 'Practice':
                return self.practice[meeting_key]
            elif session_type == 'Qualifying':
                return self.qualifying[meeting_key]
            else:
                return self.race[meeting_key]
        except KeyError:
            return None
    
    def change_date_to_timezone(self, date , timezone):
        
        dt = datetime.fromisoformat(date)
        changed_date = dt.astimezone(zoneinfo.ZoneInfo(timezone)).strftime("%A %d %B %Y") # Weekday Day Month Year

        return changed_date

    # Changes a given ISO-8601 string to the desired time zone's time
    def change_time_to_timezone(self, time , timezone):
        
        dt = datetime.fromisoformat(time)
        changed_time = dt.astimezone(zoneinfo.ZoneInfo(timezone)).strftime("%I:%M %p")

        return changed_time

    def change_start_time_to_timezone(self, meeting_key : int , session_type : AllowedSessionTypes , timezone):
        
        session = self.get_session_safely(meeting_key , session_type)

        # If data is missing return a clean placeholder instead of crashing
        if not session or 'date_start' not in session:
            return "N/A"

        return self.change_time_to_timezone(session['date_start'] , timezone)

    def change_end_time_to_timezone(self, meeting_key : int , session_type : AllowedSessionTypes , timezone):
        
        session = self.get_session_safely(meeting_key , session_type)

        # If data is missing return a clean placeholder instead of crashing
        if not session or 'date_end' not in session:
            return "N/A"

        return self.change_time_to_timezone(session['date_end'] , timezone)

    # Fetches the meeting_official_name to be displayed on the top of the GUI
    def get_meeting_official_name(self, meeting_key : int):

        meeting = self.meetings.get(meeting_key)

        return meeting['meeting_official_name'] if meeting else "Unknown Grand Prix"
