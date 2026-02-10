# ==========================================
# File: health_score.py
# Project: Smart System Health Monitor
# Description:
#   Calculates overall system health score
#   based on analyzed metrics, severity
#   levels, and configurable weights.
#   Output score is clamped to a defined
#   range (e.g., 0–100).
# ==========================================

from utils.logger import get_logger

# -------------------------------
# Initialize Logger
# -------------------------------
logger = get_logger(__name__)

# -------------------------------
# Severity to Penalty Mapping
# -------------------------------
SEVERITY_PENALTY = {
    "normal": 0,
    "warning": 25,
    "high": 50,
    "critical": 100
}

# -------------------------------
# Calculate Health Score
# -------------------------------
def calculate_health_score(
    analysis_results,
    weights,
    score_range=(0, 100)
):
    """
    Calculate overall system health score.

    Args:
        analysis_results (list):
            [
                {"metric": "cpu", "value": 80, "status": "high"},
                ...
            ]
        weights (dict):
            {
                "cpu": 0.3,
                "ram": 0.3,
                ...
            }
        score_range (tuple):
            (min_score, max_score)

    Returns:
        int: Health score within given range
    """

    if not analysis_results:
        logger.warning("No analysis results provided, returning max health score")
        return score_range[1]

    max_score = score_range[1]
    min_score = score_range[0]

    total_penalty = 0.0
    total_weight = 0.0

    for item in analysis_results:
        metric = item.get("metric")
        status = item.get("status")

        if metric not in weights:
            continue

        weight = weights.get(metric, 0)
        penalty = SEVERITY_PENALTY.get(status, 0)

        total_penalty += weight * penalty
        total_weight += weight

    if total_weight == 0:
        logger.warning("Total weight is zero, returning max health score")
        return max_score

    # Normalize penalty to score range
    normalized_penalty = (total_penalty / total_weight)

    raw_score = max_score - normalized_penalty

    # Clamp score
    final_score = max(min_score, min(int(raw_score), max_score))

    logger.info(f"Calculated Health Score: {final_score}")

    return final_score

# -------------------------------
# End of health_score.py
# -------------------------------
