# ==========================================
# File: main.py
# Project: Smart System Health Monitor
# Description:
#   Main execution service for monitoring,
#   analysis, prediction, logging, and reports
# ==========================================

import time
import sys
import signal

from core.monitor import SystemMonitor
from core.analyzer import SystemAnalyzer
from core.predictor import FailurePredictor

from utils.file_handler import append_system_log
from utils.logger import get_logger
from utils.time_utils import sleep_seconds

from reports.system_report_generator import (
    generate_daily_report,
    generate_weekly_report
)

from config.settings import (
    MONITORING_INTERVAL_SECONDS,
    ENABLE_REPORTS
)

# -------------------------------
# Initialize Logger
# -------------------------------
logger = get_logger("main")

# -------------------------------
# Graceful Shutdown Control
# -------------------------------
RUNNING = True

def handle_exit(signum, frame):
    global RUNNING
    logger.warning("Shutdown signal received. Stopping safely...")
    RUNNING = False

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

# -------------------------------
# Main Application Loop
# -------------------------------
def main():
    logger.info("🚀 Smart System Health Monitor started")

    monitor = SystemMonitor()
    analyzer = SystemAnalyzer()
    predictor = FailurePredictor()

    last_daily_report_date = None
    last_weekly_report_week = None

    while RUNNING:
        try:
            # ---------------------------
            # Collect Metrics
            # ---------------------------
            metrics = monitor.collect_metrics()

            # ---------------------------
            # Persist Raw Logs
            # ---------------------------
            append_system_log(metrics)

            # ---------------------------
            # Analyze Metrics
            # ---------------------------
            analysis_result = analyzer.analyze_metrics(metrics)

            # ---------------------------
            # Failure Prediction
            # ---------------------------
            prediction_result = predictor.predict(
                analysis_result.get("analysis", {})
            )

            # ---------------------------
            # Report Generation
            # ---------------------------
            if ENABLE_REPORTS:
                current_date = metrics["timestamp"].split(" ")[0]
                current_week = time.strftime("%Y-%W")

                if last_daily_report_date != current_date:
                    generate_daily_report(current_date)
                    last_daily_report_date = current_date

                if last_weekly_report_week != current_week:
                    generate_weekly_report()
                    last_weekly_report_week = current_week

            # ---------------------------
            # Console Summary
            # ---------------------------
            logger.info(
                f"Health Score: {analysis_result.get('health_score')} | "
                f"Failure Risk: {analysis_result.get('failure_risk')}%"
            )

        except Exception as e:
            logger.exception(f"Main loop error: {e}")

        # ---------------------------
        # Controlled Sleep
        # ---------------------------
        sleep_seconds(MONITORING_INTERVAL_SECONDS)

    logger.info("🛑 Smart System Health Monitor stopped cleanly")

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    main()
