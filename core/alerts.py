# ==========================================
# File: alerts.py
# Project: Smart System Health Monitor
# Description:
#   Handles alert generation, prioritization,
#   cooldown control, and multi-channel
#   notification (console / email / desktop).
#   Integrates with analyzer & thresholds.
# ==========================================

import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config.settings import (
    ENABLE_ALERTS,
    ALERT_COOLDOWN_SECONDS,
    ALERT_CHANNELS,
    EMAIL_ALERT_SETTINGS
)

from config.thresholds import ALERT_PRIORITY
from utils.logger import get_logger

# -------------------------------
# Initialize Logger
# -------------------------------
logger = get_logger(__name__)

# -------------------------------
# Alert Manager Class
# -------------------------------
class AlertManager:
    """
    Manages alerts with cooldown, priority,
    and multiple delivery channels.
    """

    def __init__(self):
        self.last_alert_time = {}

    # -------------------------------
    # Cooldown Check
    # -------------------------------
    def _can_send_alert(self, alert_key):
        """
        Check if alert cooldown has passed.
        """
        current_time = time.time()

        if alert_key not in self.last_alert_time:
            self.last_alert_time[alert_key] = current_time
            return True

        elapsed = current_time - self.last_alert_time[alert_key]
        if elapsed >= ALERT_COOLDOWN_SECONDS:
            self.last_alert_time[alert_key] = current_time
            return True

        return False

    # -------------------------------
    # Send Console Alert
    # -------------------------------
    def _send_console_alert(self, message, priority):
        """
        Print alert to console.
        """
        log_message = f"[ALERT - {priority}] {message}"

        if priority == "CRITICAL":
            logger.critical(log_message)
        elif priority == "HIGH":
            logger.error(log_message)
        elif priority == "MEDIUM":
            logger.warning(log_message)
        else:
            logger.info(log_message)

    # -------------------------------
    # Send Email Alert
    # -------------------------------
    def _send_email_alert(self, subject, message):
        """
        Send alert via email.
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ALERT_SETTINGS["sender_email"]
            msg["To"] = EMAIL_ALERT_SETTINGS["receiver_email"]
            msg["Subject"] = subject

            msg.attach(MIMEText(message, "plain"))

            server = smtplib.SMTP(
                EMAIL_ALERT_SETTINGS["smtp_server"],
                EMAIL_ALERT_SETTINGS["smtp_port"]
            )
            server.starttls()
            server.login(
                EMAIL_ALERT_SETTINGS["sender_email"],
                EMAIL_ALERT_SETTINGS["email_password"]
            )
            server.send_message(msg)
            server.quit()

            logger.info("Email alert sent successfully")

        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")

    # -------------------------------
    # Send Desktop Alert (Placeholder)
    # -------------------------------
    def _send_desktop_alert(self, message):
        """
        Desktop notification placeholder.
        Can be extended using plyer / notify2.
        """
        logger.info(f"[DESKTOP ALERT] {message}")

    # -------------------------------
    # Public Alert Trigger
    # -------------------------------
    def trigger_alert(self, metric_name, status, value):
        """
        Trigger alert based on metric status.
        """
        if not ENABLE_ALERTS:
            return

        priority = ALERT_PRIORITY.get(status, "LOW")
        alert_key = f"{metric_name}_{status}"

        if not self._can_send_alert(alert_key):
            return

        message = (
            f"Metric: {metric_name.upper()} | "
            f"Status: {status.upper()} | "
            f"Current Value: {value}"
        )

        # Console Alert
        if ALERT_CHANNELS.get("console", False):
            self._send_console_alert(message, priority)

        # Email Alert
        if ALERT_CHANNELS.get("email", False):
            subject = f"[{priority}] System Alert: {metric_name.upper()}"
            self._send_email_alert(subject, message)

        # Desktop Alert
        if ALERT_CHANNELS.get("desktop", False):
            self._send_desktop_alert(message)

    # -------------------------------
    # Bulk Alerts (Multiple Metrics)
    # -------------------------------
    def trigger_bulk_alerts(self, alert_list):
        """
        Trigger multiple alerts together.
        alert_list = [
            {"metric": "cpu", "status": "critical", "value": 95},
            ...
        ]
        """
        for alert in alert_list:
            self.trigger_alert(
                alert["metric"],
                alert["status"],
                alert["value"]
            )

# -------------------------------
# End of alerts.py
# -------------------------------
