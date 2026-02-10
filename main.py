# ==========================================
# File: main.py
# Project: Smart System Health Monitor
# Description:
#   Main entry point of the application.
#   Runs system monitoring, analysis,
#   prediction, logging, alerts, and
#   report generation in a continuous loop.
# ==========================================

import time
import sys
import signal
from reports.system_report_generator import generate_report

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
logger = get_logger(__name__)

# -------------------------------
# Graceful Shutdown Handler
# -------------------------------
def handle_exit(signum, frame):
    """
    Handle graceful shutdown on Ctrl+C
    """
    logger.warning("Shutdown signal received. Exiting safely...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

# -------------------------------
# Main Application Loop
# -------------------------------
def main():
    """
    Main execution loop.
    """
    logger.info("Starting Smart System Health Monitor")

    # Initialize core components
    monitor = SystemMonitor()
    analyzer = SystemAnalyzer()
    predictor = FailurePredictor()

    last_daily_report_date = None
    last_weekly_report_week = None

    while True:
        try:
            # ---------------------------
            # Collect System Metrics
            # ---------------------------
            metrics = monitor.collect_metrics()

            # ---------------------------
            # Save Raw System Logs
            # ---------------------------
            append_system_log(metrics)

            # ---------------------------
            # Analyze Metrics
            # ---------------------------
            analysis_result = analyzer.analyze_metrics(metrics)

            # ---------------------------
            # Predict Future Failure
            # ---------------------------
            prediction_result = predictor.predict(
                analysis_result["analysis"]
            )

            # ---------------------------
            # Generate Reports (Optional)
            # ---------------------------
            if ENABLE_REPORTS:
                current_date = metrics["timestamp"].split(" ")[0]
                current_week = time.strftime("%Y-%W")

                # Daily report (once per day)
                if last_daily_report_date != current_date:
                    generate_daily_report(current_date)
                    last_daily_report_date = current_date

                # Weekly report (once per week)
                if last_weekly_report_week != current_week:
                    generate_weekly_report()
                    last_weekly_report_week = current_week

            # ---------------------------
            # Console Summary (Optional)
            # ---------------------------
            logger.info(
                f"Health Score: {analysis_result['health_score']} | "
                f"Failure Risk: {analysis_result['failure_risk']}%"
            )

        except Exception as e:
            logger.error(f"Main loop error: {e}")

        # ---------------------------
        # Wait for Next Cycle
        # ---------------------------
        sleep_seconds(MONITORING_INTERVAL_SECONDS)

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    main()

# -------------------------------
# End of main.py
# -------------------------------
