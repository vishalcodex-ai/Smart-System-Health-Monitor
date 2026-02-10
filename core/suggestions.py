# ==========================================
# File: suggestions.py
# Project: Smart System Health Monitor
# Description:
#   Generates optimization and preventive
#   suggestions based on analyzed system
#   metrics and their severity levels.
#   This module provides human-readable
#   actions to improve system health and
#   reduce future failure risk.
# ==========================================

from utils.logger import get_logger

# -------------------------------
# Initialize Logger
# -------------------------------
logger = get_logger(__name__)

# -------------------------------
# Suggestion Engine Class
# -------------------------------
class SuggestionEngine:
    """
    Rule-based suggestion generator.
    Can be extended later with ML or
    adaptive recommendation logic.
    """

    def __init__(self):
        self.rules = self._load_rules()

    # -------------------------------
    # Load Suggestion Rules
    # -------------------------------
    def _load_rules(self):
        """
        Define suggestion rules for each metric
        based on severity status.
        """
        return {
            "cpu": {
                "warning": [
                    "Close unnecessary background applications.",
                    "Check for high CPU-consuming processes."
                ],
                "high": [
                    "Restart heavy applications.",
                    "Scan system for malware or runaway processes.",
                    "Consider upgrading CPU or optimizing workloads."
                ],
                "critical": [
                    "Immediate action required: stop non-essential services.",
                    "System may overheat or become unstable.",
                    "Restart system if safe to do so."
                ]
            },
            "ram": {
                "warning": [
                    "Close unused browser tabs and applications.",
                    "Monitor memory usage of running programs."
                ],
                "high": [
                    "Clear memory-intensive background services.",
                    "Increase swap memory if supported."
                ],
                "critical": [
                    "System memory exhausted — risk of crash.",
                    "Restart system and consider adding more RAM."
                ]
            },
            "disk": {
                "warning": [
                    "Clean temporary files and unused data.",
                    "Check disk usage by large folders."
                ],
                "high": [
                    "Move data to external storage.",
                    "Uninstall unused applications."
                ],
                "critical": [
                    "Disk almost full — system performance severely impacted.",
                    "Free disk space immediately or upgrade storage."
                ]
            },
            "network": {
                "warning": [
                    "Check background downloads or uploads.",
                    "Monitor network usage per application."
                ],
                "high": [
                    "Limit bandwidth-heavy applications.",
                    "Check for unauthorized network activity."
                ],
                "critical": [
                    "Possible network congestion or misuse detected.",
                    "Disconnect unnecessary devices and investigate traffic."
                ]
            },
            "temperature": {
                "warning": [
                    "Ensure proper ventilation around the system.",
                    "Clean dust from fans and vents."
                ],
                "high": [
                    "Reduce system load immediately.",
                    "Check cooling system or fan operation."
                ],
                "critical": [
                    "Critical overheating detected.",
                    "Shut down system to prevent hardware damage."
                ]
            }
        }

    # -------------------------------
    # Generate Suggestions
    # -------------------------------
    def generate(self, analysis_results):
        """
        Generate suggestions based on analysis results.

        Args:
            analysis_results (list): Output from analyzer
                [
                    {"metric": "cpu", "value": 85, "status": "high"},
                    ...
                ]

        Returns:
            list: Suggested actions (strings)
        """
        suggestions = []

        for item in analysis_results:
            metric = item.get("metric")
            status = item.get("status")

            if metric in self.rules:
                metric_rules = self.rules[metric]
                if status in metric_rules:
                    suggestions.extend(metric_rules[status])

        # Remove duplicates while preserving order
        unique_suggestions = list(dict.fromkeys(suggestions))

        if unique_suggestions:
            logger.info(
                f"Generated {len(unique_suggestions)} optimization suggestions"
            )

        return unique_suggestions

# -------------------------------
# End of suggestions.py
# -------------------------------
