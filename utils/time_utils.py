# ==========================================
# File: time_utils.py
# Project: Smart System Health Monitor
# Description:
#   Time and date utility functions used
#   across monitoring, logging, reporting,
#   scheduling, and ML data handling.
# ==========================================

from datetime import datetime, timedelta
import time

# -------------------------------
# Get Current Timestamp (String)
# -------------------------------
def get_current_timestamp():
    """
    Get current timestamp as string.
    Format: YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# -------------------------------
# Get Current Date (String)
# -------------------------------
def get_current_date():
    """
    Get current date as string.
    Format: YYYY-MM-DD
    """
    return datetime.now().strftime("%Y-%m-%d")

# -------------------------------
# Get Unix Timestamp
# -------------------------------
def get_unix_timestamp():
    """
    Get current Unix timestamp (seconds).
    """
    return int(time.time())

# -------------------------------
# Sleep Helper
# -------------------------------
def sleep_seconds(seconds):
    """
    Pause execution for given seconds.
    Safe wrapper around time.sleep().
    """
    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        pass

# -------------------------------
# Check If Same Day
# -------------------------------
def is_same_day(ts1, ts2):
    """
    Check if two timestamps are on same day.

    Args:
        ts1 (str): 'YYYY-MM-DD HH:MM:SS'
        ts2 (str): 'YYYY-MM-DD HH:MM:SS'

    Returns:
        bool
    """
    d1 = datetime.strptime(ts1, "%Y-%m-%d %H:%M:%S").date()
    d2 = datetime.strptime(ts2, "%Y-%m-%d %H:%M:%S").date()
    return d1 == d2

# -------------------------------
# Check If New Day Started
# -------------------------------
def is_new_day(last_timestamp):
    """
    Check if current time is a new day
    compared to last timestamp.
    """
    last_date = datetime.strptime(
        last_timestamp, "%Y-%m-%d %H:%M:%S"
    ).date()
    return datetime.now().date() != last_date

# -------------------------------
# Get Start & End of Day
# -------------------------------
def get_day_range(date_str=None):
    """
    Get start and end datetime of a day.

    Args:
        date_str (str): YYYY-MM-DD (optional)

    Returns:
        tuple(datetime, datetime)
    """
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.now()

    start = datetime.combine(date.date(), datetime.min.time())
    end = datetime.combine(date.date(), datetime.max.time())

    return start, end

# -------------------------------
# Get Start & End of Week
# -------------------------------
def get_week_range(date_str=None):
    """
    Get start and end datetime of the week.
    Week starts on Monday.
    """
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.now()

    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)

    start = datetime.combine(start.date(), datetime.min.time())
    end = datetime.combine(end.date(), datetime.max.time())

    return start, end

# -------------------------------
# Convert Seconds to HH:MM:SS
# -------------------------------
def seconds_to_hms(seconds):
    """
    Convert seconds to HH:MM:SS format.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(secs):02}"

# -------------------------------
# End of time_utils.py
# -------------------------------
