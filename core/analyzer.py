# ==========================================
# File: analyzer.py
# Project: Smart System Health Monitor
# Description:
#   Analyzes real-time system metrics,
#   compares them with thresholds,
#   calculates health score,
#   triggers alerts, and generates
#   optimization suggestions.
# ==========================================

from config.thresholds import (
    THRESHOLD_MAP,
    FAILURE_RISK_THRESHOLDS,
    get_status
)

from config.settings import (
    AUTO_SUGGEST_OPTIMIZATION,
    HEALTH_SCORE_WEIGHTS,
    HEALTH_SCORE_RANGE
)

from core.alerts import AlertManager
from core.suggestions import SuggestionEngine
from utils.logger import get_logger
from utils.health_score import calculate_health_score

# -------------------------------
# Initialize Components
# -------------------------------
logger = get_logger(__name__)
alert_manager = AlertManager()
suggestion_engine = SuggestionEngine()

# -------------------------------
# System Analyzer Class
# -------------------------------
class SystemAnalyzer:
    """
    Analyzes system metrics, determines status,
    health score, alerts, and suggestions.
    """

    def __init__(self):
        self.last_analysis = {}

    # -------------------------------
    # Analyze Single Metric
    # -------------------------------
    def _analyze_metric(self, metric_name, value):
        """
        Analyze a single metric against thresholds.
        """
        if metric_name not in THRESHOLD_MAP or value is None:
            return None

        thresholds = THRESHOLD_MAP[metric_name]
        status = get_status(value, thresholds)

        return {
            "metric": metric_name,
            "value": value,
            "status": status
        }

    # -------------------------------
    # Analyze All Metrics
    # -------------------------------
    def analyze_metrics(self, metrics):
        """
        Analyze full system metrics snapshot.
        """
        analysis_results = []
        alert_queue = []

        # ---------------------------
        # CPU
        # ---------------------------
        if metrics.get("cpu") is not None:
            cpu_result = self._analyze_metric("cpu", metrics["cpu"])
            if cpu_result:
                analysis_results.append(cpu_result)
                if cpu_result["status"] != "normal":
                    alert_queue.append(cpu_result)

        # ---------------------------
        # RAM
        # ---------------------------
        if metrics.get("ram"):
            ram_percent = metrics["ram"]["percent"]
            ram_result = self._analyze_metric("ram", ram_percent)
            if ram_result:
                analysis_results.append(ram_result)
                if ram_result["status"] != "normal":
                    alert_queue.append(ram_result)

        # ---------------------------
        # Disk
        # ---------------------------
        if metrics.get("disk"):
            disk_percent = metrics["disk"]["percent"]
            disk_result = self._analyze_metric("disk", disk_percent)
            if disk_result:
                analysis_results.append(disk_result)
                if disk_result["status"] != "normal":
                    alert_queue.append(disk_result)

        # ---------------------------
        # Network
        # ---------------------------
        if metrics.get("network"):
            net_value = (
                metrics["network"]["upload_mb_s"] +
                metrics["network"]["download_mb_s"]
            )
            net_result = self._analyze_metric("network", net_value)
            if net_result:
                analysis_results.append(net_result)
                if net_result["status"] != "normal":
                    alert_queue.append(net_result)

        # ---------------------------
        # Temperature
        # ---------------------------
        if metrics.get("temperature") is not None:
            temp_result = self._analyze_metric(
                "temperature", metrics["temperature"]
            )
            if temp_result:
                analysis_results.append(temp_result)
                if temp_result["status"] != "normal":
                    alert_queue.append(temp_result)

        # ---------------------------
        # Trigger Alerts
        # ---------------------------
        for alert in alert_queue:
            alert_manager.trigger_alert(
                alert["metric"],
                alert["status"],
                alert["value"]
            )

        # ---------------------------
        # Health Score Calculation
        # ---------------------------
        health_score = calculate_health_score(
            analysis_results,
            HEALTH_SCORE_WEIGHTS,
            HEALTH_SCORE_RANGE
        )

        # ---------------------------
        # Suggestions
        # ---------------------------
        suggestions = []
        if AUTO_SUGGEST_OPTIMIZATION:
            suggestions = suggestion_engine.generate(analysis_results)

        # ---------------------------
        # Failure Risk Estimation
        # ---------------------------
        failure_risk = self._estimate_failure_risk(analysis_results)

        self.last_analysis = {
            "analysis": analysis_results,
            "health_score": health_score,
            "suggestions": suggestions,
            "failure_risk": failure_risk
        }

        logger.info(
            f"Analysis completed | Health Score: {health_score} | "
            f"Failure Risk: {failure_risk}%"
        )

        return self.last_analysis

    # -------------------------------
    # Failure Risk Estimation
    # -------------------------------
    def _estimate_failure_risk(self, analysis_results):
        """
        Estimate failure risk percentage based on metric severity.
        """
        risk = 0

        for item in analysis_results:
            if item["status"] == "warning":
                risk += 10
            elif item["status"] == "high":
                risk += 20
            elif item["status"] == "critical":
                risk += 35

        # Clamp risk to 100%
        risk = min(risk, 100)

        # Map to failure risk levels
        for level, threshold in FAILURE_RISK_THRESHOLDS.items():
            if risk <= threshold:
                return risk

        return risk

# -------------------------------
# End of analyzer.py
# -------------------------------
