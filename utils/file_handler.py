# ==========================================
# File: file_handler.py
# Project: Smart System Health Monitor
# Description:
#   Handles all file read/write operations
#   such as system logs, daily stats,
#   prediction data, and backups.
#   Ensures safe CSV operations and
#   directory availability.
# ==========================================

import os
import csv
import shutil
from datetime import datetime

from config.paths import (
    SYSTEM_LOG_FILE,
    PREDICTION_DATA_FILE,
    DAILY_STATS_FILE,
    BACKUP_DIR
)

from utils.logger import get_logger

# -------------------------------
# Initialize Logger
# -------------------------------
logger = get_logger(__name__)

# -------------------------------
# Ensure Directory Exists
# -------------------------------
def _ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

# -------------------------------
# Ensure CSV File Exists
# -------------------------------
def _ensure_csv(file_path, headers):
    """
    Ensure CSV file exists with headers.
    """
    _ensure_dir(file_path)

    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
        logger.info(f"Created new CSV file: {file_path}")

# -------------------------------
# Append System Metrics Log
# -------------------------------
def append_system_log(metrics):
    """
    Append system metrics snapshot to CSV.
    """
    headers = [
        "timestamp",
        "cpu",
        "ram_percent",
        "disk_percent",
        "network_mb_s",
        "temperature",
        "process_count"
    ]

    _ensure_csv(SYSTEM_LOG_FILE, headers)

    row = {
        "timestamp": metrics.get("timestamp"),
        "cpu": metrics.get("cpu"),
        "ram_percent": metrics.get("ram", {}).get("percent"),
        "disk_percent": metrics.get("disk", {}).get("percent"),
        "network_mb_s": (
            metrics.get("network", {}).get("upload_mb_s", 0) +
            metrics.get("network", {}).get("download_mb_s", 0)
        ),
        "temperature": metrics.get("temperature"),
        "process_count": metrics.get("process_count")
    }

    with open(SYSTEM_LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(row)

# -------------------------------
# Append Daily Statistics
# -------------------------------
def append_daily_stats(stats):
    """
    Append daily aggregated stats.
    """
    headers = [
        "date",
        "avg_cpu",
        "avg_ram",
        "avg_disk",
        "avg_network",
        "avg_temperature",
        "health_score"
    ]

    _ensure_csv(DAILY_STATS_FILE, headers)

    with open(DAILY_STATS_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(stats)

# -------------------------------
# Append Prediction Data
# -------------------------------
def append_prediction_data(record):
    """
    Append ML prediction data for retraining.
    """
    headers = [
        "timestamp",
        "failure_probability",
        "confidence"
    ]

    _ensure_csv(PREDICTION_DATA_FILE, headers)

    with open(PREDICTION_DATA_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(record)

# -------------------------------
# Backup Old Logs
# -------------------------------
def backup_system_logs():
    """
    Backup system log CSV with timestamp.
    """
    if not os.path.exists(SYSTEM_LOG_FILE):
        logger.warning("No system log file found for backup")
        return

    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(
        BACKUP_DIR,
        f"system_logs_backup_{timestamp}.csv"
    )

    shutil.copy2(SYSTEM_LOG_FILE, backup_file)
    logger.info(f"System logs backed up to {backup_file}")

# -------------------------------
# Read CSV File
# -------------------------------
def read_csv(file_path):
    """
    Read CSV file and return list of rows.
    """
    if not os.path.exists(file_path):
        return []

    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

# -------------------------------
# Clear CSV File (Keep Header)
# -------------------------------
def clear_csv(file_path):
    """
    Clear CSV data but keep header.
    """
    if not os.path.exists(file_path):
        return

    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader, None)

    if headers:
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

        logger.info(f"Cleared CSV file data: {file_path}")

# -------------------------------
# End of file_handler.py
# -------------------------------
