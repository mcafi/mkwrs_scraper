import re

def parse_time(time):
    time_regex = r"(\d+)?\'?(\d+)\"(\d+)"
    if (not re.match(time_regex, time)):
        return None
    time_match = re.search(time_regex, time)
    minutes = time_match.group(1)
    seconds = time_match.group(2)
    milliseconds = time_match.group(3)
    return 60 * int(minutes) + int(seconds) + int(milliseconds) / 1000

def parse_lap_time(lap_time):
    time_regex = r"(\d+).(\d+)"
    if (not re.match(time_regex, lap_time)):
        return None
    time_match = re.search(time_regex, lap_time)
    seconds = time_match.group(1)
    milliseconds = time_match.group(2)
    return int(seconds) + int(milliseconds) / 1000