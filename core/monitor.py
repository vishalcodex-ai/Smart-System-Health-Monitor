# ==========================================
# File: monitor.py
# Project: Smart System Health Monitor
# Description:
#   Collects real-time system metrics such as
#   CPU, RAM, Disk, Network, Temperature,
#   Process Count, and Load Average.
#   This module acts as the data source for
#   analyzer, predictor, alerts, and dashboard.
# ==========================================

import psutil
import platform
import time
import os

from config.settings import (
    MONITOR_CPU,
    MONITOR_RAM,
    MONITOR_DISK,
    MONITOR_NETWORK,
    MONITOR_TEMPERATURE,
    MONITORING_INTERVAL_SECONDS
)

# -------------------------------
# System Monitor Class
# -------------------------------
class SystemMonitor:
    """
    Collects system health metrics in real-time.
    """

    def __init__(self):
        self.system_info = self._get_system_info()
        self.last_network_stats = psutil.net_io_counters()

    # -------------------------------
    # System Info
    # -------------------------------
    def _get_system_info(self):
        """
        Get static system information.
        """
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "cpu_cores_logical": psutil.cpu_count(logical=True),
            "cpu_cores_physical": psutil.cpu_count(logical=False),
            "total_ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2)
        }

    # -------------------------------
    # CPU Metrics
    # -------------------------------
    def get_cpu_usage(self):
        """
        Get CPU usage percentage.
        """
        if not MONITOR_CPU:
            return None

        return psutil.cpu_percent(interval=1)

    # -------------------------------
    # RAM Metrics
    # -------------------------------
    def get_ram_usage(self):
        """
        Get RAM usage details.
        """
        if not MONITOR_RAM:
            return None

        mem = psutil.virtual_memory()
        return {
            "total_gb": round(mem.total / (1024 ** 3), 2),
            "used_gb": round(mem.used / (1024 ** 3), 2),
            "available_gb": round(mem.available / (1024 ** 3), 2),
            "percent": mem.percent
        }

    # -------------------------------
    # Disk Metrics
    # -------------------------------
    def get_disk_usage(self):
        """
        Get Disk usage details.
        """
        if not MONITOR_DISK:
            return None

        disk = psutil.disk_usage("/")
        return {
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "free_gb": round(disk.free / (1024 ** 3), 2),
            "percent": disk.percent
        }

    # -------------------------------
    # Network Metrics
    # -------------------------------
    def get_network_usage(self):
        """
        Calculate network upload/download speed.
        """
        if not MONITOR_NETWORK:
            return None

        current = psutil.net_io_counters()
        sent_bytes = current.bytes_sent - self.last_network_stats.bytes_sent
        recv_bytes = current.bytes_recv - self.last_network_stats.bytes_recv

        self.last_network_stats = current

        return {
            "upload_mb_s": round((sent_bytes / 1024 / 1024), 3),
            "download_mb_s": round((recv_bytes / 1024 / 1024), 3)
        }

    # -------------------------------
    # Temperature Metrics
    # -------------------------------
    def get_temperature(self):
        """
        Get CPU temperature (if supported).
        """
        if not MONITOR_TEMPERATURE:
            return None

        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return None

            for name, entries in temps.items():
                for entry in entries:
                    if entry.current:
                        return round(entry.current, 2)
        except Exception:
            return None

        return None

    # -------------------------------
    # Process Count
    # -------------------------------
    def get_process_count(self):
        """
        Get total number of running processes.
        """
        return len(psutil.pids())

    # -------------------------------
    # Load Average
    # -------------------------------
    def get_load_average(self):
        """
        Get system load average (Unix only).
        """
        if hasattr(os, "getloadavg"):
            load1, load5, load15 = os.getloadavg()
            return {
                "1_min": round(load1, 2),
                "5_min": round(load5, 2),
                "15_min": round(load15, 2)
            }
        return None

    # -------------------------------
    # Collect All Metrics
    # -------------------------------
    def collect_metrics(self):
        """
        Collect all enabled system metrics.
        """
        metrics = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": self.system_info,
            "cpu": self.get_cpu_usage(),
            "ram": self.get_ram_usage(),
            "disk": self.get_disk_usage(),
            "network": self.get_network_usage(),
            "temperature": self.get_temperature(),
            "process_count": self.get_process_count(),
            "load_average": self.get_load_average()
        }

        return metrics

    # -------------------------------
    # Continuous Monitoring Generator
    # -------------------------------
    def stream_metrics(self):
        """
        Generator for continuous monitoring.
        """
        while True:
            yield self.collect_metrics()
            time.sleep(MONITORING_INTERVAL_SECONDS)

# -------------------------------
# End of monitor.py
# -------------------------------
