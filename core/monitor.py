# ==========================================
# File: core/monitor.py
# Smart System Health Monitor
# ==========================================

import time
import platform
import psutil
from datetime import datetime

MONITORING_INTERVAL_SECONDS = 3


class SystemMonitor:
    def __init__(self):
        self.system_info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "cpu_cores": psutil.cpu_count(logical=True),
        }

        # 🔥 IMPORTANT: warm-up call (psutil requirement)
        psutil.cpu_percent(interval=None)

    # -------------------------------
    # CPU Usage
    # -------------------------------
    def get_cpu_usage(self):
        """
        Returns real CPU usage percentage.
        interval=1 avoids always-0 bug.
        """
        return psutil.cpu_percent(interval=1)

    # -------------------------------
    # RAM Usage
    # -------------------------------
    def get_ram_usage(self):
        mem = psutil.virtual_memory()
        return {
            "total": round(mem.total / (1024 ** 3), 2),
            "used": round(mem.used / (1024 ** 3), 2),
            "percent": mem.percent
        }

    # -------------------------------
    # Disk Usage
    # -------------------------------
    def get_disk_usage(self):
        disk = psutil.disk_usage("/")
        return {
            "total": round(disk.total / (1024 ** 3), 2),
            "used": round(disk.used / (1024 ** 3), 2),
            "percent": disk.percent
        }

    # -------------------------------
    # Network Usage
    # -------------------------------
    def get_network_usage(self):
        net = psutil.net_io_counters()
        return {
            "bytes_sent_mb": round(net.bytes_sent / (1024 ** 2), 2),
            "bytes_recv_mb": round(net.bytes_recv / (1024 ** 2), 2)
        }

    # -------------------------------
    # CPU Temperature (Linux only)
    # -------------------------------
    def get_temperature(self):
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return None

            for name in temps:
                if temps[name]:
                    return temps[name][0].current
        except Exception:
            return None

        return None

    # -------------------------------
    # Process Count
    # -------------------------------
    def get_process_count(self):
        return len(psutil.pids())

    # -------------------------------
    # Load Average (Linux / Unix only)
    # -------------------------------
    def get_load_average(self):
        try:
            return {
                "1_min": psutil.getloadavg()[0],
                "5_min": psutil.getloadavg()[1],
                "15_min": psutil.getloadavg()[2],
            }
        except (AttributeError, OSError):
            # Windows / unsupported OS
            return None

    # -------------------------------
    # Collect All Metrics
    # -------------------------------
    def collect_metrics(self):
        try:
            # -----------------------
            # CPU
            # -----------------------
            cpu = psutil.cpu_percent(interval=1)

            # -----------------------
            # RAM
            # -----------------------
            mem = psutil.virtual_memory()
            ram = {
                "total": round(mem.total / (1024**3), 2),
                "used": round(mem.used / (1024**3), 2),
                "percent": mem.percent
            }

            # -----------------------
            # Disk
            # -----------------------
            disk_usage = psutil.disk_usage("/")
            disk = {
                "total": round(disk_usage.total / (1024**3), 2),
                "used": round(disk_usage.used / (1024**3), 2),
                "percent": disk_usage.percent
            }

            # -----------------------
            # Network (SAFE)
            # -----------------------
            net1 = psutil.net_io_counters()
            time.sleep(1)
            net2 = psutil.net_io_counters()

            upload_mb_s = round(
                (net2.bytes_sent - net1.bytes_sent) / (1024**2), 3
            )
            download_mb_s = round(
                (net2.bytes_recv - net1.bytes_recv) / (1024**2), 3
            )

            network = {
                "upload_mb_s": max(upload_mb_s, 0),
                "download_mb_s": max(download_mb_s, 0)
            }

            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cpu": cpu,
                "ram": ram,
                "disk": disk,
                "network": network
            }

        except Exception as e:
            return {
                "error": str(e)
            }
    
    def get_metrics(self):
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            return {
                "cpu": cpu,
                "ram": ram,
                "disk": disk
            }
        except Exception as e:
            return {
                "error": str(e)
            }
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
