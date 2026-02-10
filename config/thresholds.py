# ==========================================
# File: thresholds.py
# Project: Smart System Health Monitor
# Description:
#   Defines all threshold limits for system
#   resources such as CPU, RAM, Disk,
#   Network, and Temperature.
#   These thresholds are used for:
#   - Alerts
#   - Health score calculation
#   - Failure prediction triggers
# ==========================================

# -------------------------------
# CPU Usage Thresholds (%)
# -------------------------------
CPU_THRESHOLDS = {
    "normal": 0,
    "warning": 60,
    "high": 75,
    "critical": 90
}

# -------------------------------
# RAM Usage Thresholds (%)
# -------------------------------
RAM_THRESHOLDS = {
    "normal": 0,
    "warning": 65,
    "high": 80,
    "critical": 90
}

# -------------------------------
# Disk Usage Thresholds (%)
# -------------------------------
DISK_THRESHOLDS = {
    "normal": 0,
    "warning": 70,
    "high": 85,
    "critical": 95
}

# -------------------------------
# Network Usage Thresholds (MB/s)
# -------------------------------
NETWORK_THRESHOLDS = {
    "normal": 0,
    "warning": 5,
    "high": 10,
    "critical": 20
}

# -------------------------------
# Temperature Thresholds (°C)
# -------------------------------
TEMPERATURE_THRESHOLDS = {
    "normal": 0,
    "warning": 60,
    "high": 75,
    "critical": 85
}

# -------------------------------
# Disk I/O Thresholds (MB/s)
# -------------------------------
DISK_IO_THRESHOLDS = {
    "normal": 0,
    "warning": 50,
    "high": 100,
    "critical": 200
}

# -------------------------------
# Process Count Thresholds
# -------------------------------
PROCESS_COUNT_THRESHOLDS = {
    "normal": 0,
    "warning": 200,
    "high": 300,
    "critical": 400
}

# -------------------------------
# Load Average Thresholds
# (Linux / Unix based systems)
# -------------------------------
LOAD_AVERAGE_THRESHOLDS = {
    "normal": 0,
    "warning": 1.5,
    "high": 3.0,
    "critical": 5.0
}

# -------------------------------
# Failure Risk Score Thresholds (%)
# Used by ML Predictor
# -------------------------------
FAILURE_RISK_THRESHOLDS = {
    "low": 0,
    "medium": 40,
    "high": 70,
    "critical": 90
}

# -------------------------------
# Alert Priority Mapping
# -------------------------------
ALERT_PRIORITY = {
    "normal": "LOW",
    "warning": "MEDIUM",
    "high": "HIGH",
    "critical": "CRITICAL"
}

# -------------------------------
# Unified Threshold Map
# (Used for dynamic access)
# -------------------------------
THRESHOLD_MAP = {
    "cpu": CPU_THRESHOLDS,
    "ram": RAM_THRESHOLDS,
    "disk": DISK_THRESHOLDS,
    "network": NETWORK_THRESHOLDS,
    "temperature": TEMPERATURE_THRESHOLDS,
    "disk_io": DISK_IO_THRESHOLDS,
    "process_count": PROCESS_COUNT_THRESHOLDS,
    "load_average": LOAD_AVERAGE_THRESHOLDS
}

# -------------------------------
# Helper Function
# -------------------------------
def get_status(value, threshold_dict):
    """
    Determine status level based on value
    and given threshold dictionary.

    Args:
        value (float): Current metric value
        threshold_dict (dict): Threshold config

    Returns:
        str: normal | warning | high | critical
    """
    if value >= threshold_dict["critical"]:
        return "critical"
    elif value >= threshold_dict["high"]:
        return "high"
    elif value >= threshold_dict["warning"]:
        return "warning"
    else:
        return "normal"

# -------------------------------
# End of thresholds.py
# -------------------------------
