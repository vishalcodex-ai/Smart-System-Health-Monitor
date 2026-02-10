# ==========================================
# File: paths.py
# Project: Smart System Health Monitor
# Description:
#   Centralized file & directory paths
# ==========================================

import os

# -------------------------------
# Base Directory
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------
# Data Directories
# -------------------------------
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# -------------------------------
# Data Files
# -------------------------------
SYSTEM_LOG_FILE = os.path.join(DATA_DIR, "system_logs.csv")
PREDICTION_DATA_FILE = os.path.join(DATA_DIR, "prediction_data.csv")
DAILY_STATS_FILE = os.path.join(DATA_DIR, "daily_stats.csv")

# -------------------------------
# End of paths.py
# -------------------------------
