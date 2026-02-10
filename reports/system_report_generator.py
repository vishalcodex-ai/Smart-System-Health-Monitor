# ==========================================
# File: system_report_generator.py
# Project: Smart System Health Monitor
# Description:
#   Generates daily and weekly system
#   health reports from collected CSV data.
#   Reports include averages, health score,
#   alerts summary, and failure risk insights.
# ==========================================

import os
from datetime import datetime, timedelta

from config.paths import (
    SYSTEM_LOG_FILE,
    DAILY_STATS_FILE,
    DAILY_REPORT,
    WEEKLY_REPORT
)

from utils.file_handler import read_csv, append_daily_stats
from utils.health_score import calculate_health_score
from utils.logger import get_logger

# -------------------------------
# Initialize Logger
# -------------------------------
logger = get_logger(__name__)

# -------------------------------
# Helper: Safe Float
# -------------------------------
def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

# -------------------------------
# Compute Averages
# -------------------------------
def _compute_averages(rows):
    """
    Compute average metrics from CSV rows.
    """
    if not rows:
        return {}

    total = {
        "cpu": 0.0,
        "ram_percent": 0.0,
        "disk_percent": 0.0,
        "network_mb_s": 0.0,
        "temperature": 0.0
    }

    for r in rows:
        total["cpu"] += _to_float(r.get("cpu"))
        total["ram_percent"] += _to_float(r.get("ram_percent"))
        total["disk_percent"] += _to_float(r.get("disk_percent"))
        total["network_mb_s"] += _to_float(r.get("network_mb_s"))
        total["temperature"] += _to_float(r.get("temperature"))

    count = len(rows)

    return {
        "avg_cpu": round(total["cpu"] / count, 2),
        "avg_ram": round(total["ram_percent"] / count, 2),
        "avg_disk": round(total["disk_percent"] / count, 2),
        "avg_network": round(total["network_mb_s"] / count, 2),
        "avg_temperature": round(total["temperature"] / count, 2)
    }

# -------------------------------
# Filter Rows By Date Range
# -------------------------------
def _filter_rows_by_date(rows, start_date, end_date):
    """
    Filter CSV rows by date range (inclusive).
    """
    filtered = []
    for r in rows:
        ts = r.get("timestamp")
        if not ts:
            continue
        try:
            dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            if start_date <= dt <= end_date:
                filtered.append(r)
        except ValueError:
            continue
    return filtered

# -------------------------------
# Generate Daily Report
# -------------------------------
def generate_daily_report(date=None):
    """
    Generate daily system report.
    """
    if not os.path.exists(SYSTEM_LOG_FILE):
        logger.warning("No system log data found for daily report")
        return

    rows = read_csv(SYSTEM_LOG_FILE)

    if not rows:
        logger.warning("System log is empty, daily report skipped")
        return

    if date:
        report_date = datetime.strptime(date, "%Y-%m-%d").date()
    else:
        report_date = datetime.now().date()

    start = datetime.combine(report_date, datetime.min.time())
    end = datetime.combine(report_date, datetime.max.time())

    day_rows = _filter_rows_by_date(rows, start, end)
    averages = _compute_averages(day_rows)

    if not averages:
        logger.warning("No data for selected day")
        return

    # Health score (simple mapping)
    analysis_results = [
        {"metric": "cpu", "status": "normal", "value": averages["avg_cpu"]},
        {"metric": "ram", "status": "normal", "value": averages["avg_ram"]},
        {"metric": "disk", "status": "normal", "value": averages["avg_disk"]},
        {"metric": "network", "status": "normal", "value": averages["avg_network"]},
        {"metric": "temperature", "status": "normal", "value": averages["avg_temperature"]}
    ]

    # Equal weights fallback
    weights = {
        "cpu": 0.3,
        "ram": 0.3,
        "disk": 0.25,
        "network": 0.1,
        "temperature": 0.05
    }

    health_score = calculate_health_score(analysis_results, weights)

    # Save daily stats CSV
    append_daily_stats({
        "date": report_date.strftime("%Y-%m-%d"),
        "avg_cpu": averages["avg_cpu"],
        "avg_ram": averages["avg_ram"],
        "avg_disk": averages["avg_disk"],
        "avg_network": averages["avg_network"],
        "avg_temperature": averages["avg_temperature"],
        "health_score": health_score
    })

    # Write report file
    with open(DAILY_REPORT, "w", encoding="utf-8") as f:
        f.write("===== DAILY SYSTEM HEALTH REPORT =====\n")
        f.write(f"Date           : {report_date}\n\n")
        f.write(f"Average CPU    : {averages['avg_cpu']}%\n")
        f.write(f"Average RAM    : {averages['avg_ram']}%\n")
        f.write(f"Average Disk   : {averages['avg_disk']}%\n")
        f.write(f"Average Network: {averages['avg_network']} MB/s\n")
        f.write(f"Average Temp   : {averages['avg_temperature']} °C\n\n")
        f.write(f"Health Score   : {health_score}/100\n")
        f.write("=====================================\n")

    logger.info(f"Daily report generated: {DAILY_REPORT}")

# -------------------------------
# Generate Weekly Report
# -------------------------------
def generate_weekly_report():
    """
    Generate weekly system report (last 7 days).
    """
    if not os.path.exists(SYSTEM_LOG_FILE):
        logger.warning("No system log data found for weekly report")
        return

    rows = read_csv(SYSTEM_LOG_FILE)

    if not rows:
        logger.warning("System log is empty, weekly report skipped")
        return

    end = datetime.now()
    start = end - timedelta(days=7)

    week_rows = _filter_rows_by_date(rows, start, end)
    averages = _compute_averages(week_rows)

    if not averages:
        logger.warning("No data for last 7 days")
        return

    with open(WEEKLY_REPORT, "w", encoding="utf-8") as f:
        f.write("===== WEEKLY SYSTEM HEALTH REPORT =====\n")
        f.write(f"Period         : Last 7 Days\n\n")
        f.write(f"Avg CPU        : {averages['avg_cpu']}%\n")
        f.write(f"Avg RAM        : {averages['avg_ram']}%\n")
        f.write(f"Avg Disk       : {averages['avg_disk']}%\n")
        f.write(f"Avg Network    : {averages['avg_network']} MB/s\n")
        f.write(f"Avg Temp       : {averages['avg_temperature']} °C\n")
        f.write("======================================\n")

    logger.info(f"Weekly report generated: {WEEKLY_REPORT}")

# -------------------------------
# CLI Entry
# -------------------------------
if __name__ == "__main__":
    generate_daily_report()
    generate_weekly_report()

# -------------------------------
# End of system_report_generator.py
# -------------------------------
