# ==========================================
# File: settings.py
# Project: Smart System Health Monitor
# Description:
#   Central configuration file for the
#   entire system health monitoring project.
#   Controls system behavior, monitoring
#   intervals, logging, ML usage, dashboard,
#   alerts, and reporting settings.
# ==========================================

import os

# -------------------------------
# Project Root Path
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------
# Application Info
# -------------------------------
APP_NAME = "Smart System Health Monitor"
APP_VERSION = "1.0.0"
ENVIRONMENT = "development"   # development | production

# -------------------------------
# System Monitoring Settings
# -------------------------------
MONITORING_INTERVAL_SECONDS = 5     # System stats refresh time
SAVE_STATS_INTERVAL_SECONDS = 60    # Save stats to CSV
ENABLE_REALTIME_MONITORING = True

# -------------------------------
# Hardware Metrics Toggles
# -------------------------------
MONITOR_CPU = True
MONITOR_RAM = True
MONITOR_DISK = True
MONITOR_NETWORK = True
MONITOR_TEMPERATURE = True

# -------------------------------
# Logging Configuration
# -------------------------------
LOG_LEVEL = "INFO"   # DEBUG | INFO | WARNING | ERROR | CRITICAL
LOG_TO_FILE = True
LOG_TO_CONSOLE = True

LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE_NAME = "system_health.log"

# Ensure log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

# -------------------------------
# Data Storage Paths
# -------------------------------
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKUP_DIR = os.path.join(DATA_DIR, "backup")

SYSTEM_LOG_FILE = os.path.join(DATA_DIR, "system_logs.csv")
DAILY_STATS_FILE = os.path.join(DATA_DIR, "daily_stats.csv")
PREDICTION_DATA_FILE = os.path.join(DATA_DIR, "prediction_data.csv")

# Create data directories if missing
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# -------------------------------
# Alert System Settings
# -------------------------------
ENABLE_ALERTS = True
ALERT_COOLDOWN_SECONDS = 300   # Avoid repeated alerts

ALERT_CHANNELS = {
    "console": True,
    "email": False,
    "desktop": False
}

# -------------------------------
# Email Alert Configuration
# -------------------------------
EMAIL_ALERT_SETTINGS = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your_email@gmail.com",
    "receiver_email": "receiver_email@gmail.com",
    "email_password": "your_app_password"
}

# -------------------------------
# Machine Learning Settings
# -------------------------------
ENABLE_ML_PREDICTION = True
ML_MODEL_PATH = os.path.join(BASE_DIR, "ml", "model.pkl")
ML_RETRAIN_INTERVAL_DAYS = 7

PREDICTION_CONFIDENCE_THRESHOLD = 0.75  # 75% confidence

# -------------------------------
# Health Score Settings
# -------------------------------
HEALTH_SCORE_RANGE = (0, 100)

HEALTH_SCORE_WEIGHTS = {
    "cpu": 0.30,
    "ram": 0.30,
    "disk": 0.25,
    "network": 0.10,
    "temperature": 0.05
}

# -------------------------------
# Dashboard Settings
# -------------------------------
DASHBOARD_HOST = "127.0.0.1"
DASHBOARD_PORT = 5000
DASHBOARD_DEBUG = True

# -------------------------------
# Reporting Settings
# -------------------------------
ENABLE_REPORTS = True

REPORT_DIR = os.path.join(BASE_DIR, "reports")
DAILY_REPORT_FILE = os.path.join(REPORT_DIR, "daily_report.txt")
WEEKLY_REPORT_FILE = os.path.join(REPORT_DIR, "weekly_report.txt")

os.makedirs(REPORT_DIR, exist_ok=True)

# -------------------------------
# Auto Run & Background Jobs
# -------------------------------
ENABLE_AUTO_RUN = True
AUTO_RUN_ON_BOOT = False

# -------------------------------
# Safety & Fail-Safe Settings
# -------------------------------
MAX_CPU_USAGE_BEFORE_ACTION = 95
MAX_RAM_USAGE_BEFORE_ACTION = 95
MAX_DISK_USAGE_BEFORE_ACTION = 90

AUTO_SUGGEST_OPTIMIZATION = True
AUTO_SHUTDOWN_ON_CRITICAL = False

# -------------------------------
# Debug Flags
# -------------------------------
DEBUG_PRINT_RAW_STATS = False
DEBUG_SAVE_FAKE_DATA = False

# -------------------------------
# End of settings.py
# -------------------------------
