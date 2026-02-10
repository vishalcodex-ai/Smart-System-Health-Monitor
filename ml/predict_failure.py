# ==========================================
# File: predict_failure.py
# Project: Smart System Health Monitor
# Description:
#   Uses trained ML model to predict
#   system failure risk from given
#   system metrics.
#   Can be used:
#   - As a standalone script
#   - As an imported module
# ==========================================

import os
import pickle
import argparse
import numpy as np

from config.paths import ML_MODEL_FILE
from utils.logger import get_logger

# -------------------------------
# Initialize Logger
# -------------------------------
logger = get_logger(__name__)

# -------------------------------
# Load Trained Model
# -------------------------------
def load_model():
    """
    Load trained ML model from disk.
    """
    if not os.path.exists(ML_MODEL_FILE):
        raise FileNotFoundError(
            f"ML model not found at {ML_MODEL_FILE}. "
            "Please train the model first."
        )

    with open(ML_MODEL_FILE, "rb") as f:
        model = pickle.load(f)

    logger.info("ML model loaded successfully")
    return model

# -------------------------------
# Prepare Feature Vector
# -------------------------------
def prepare_features(
    cpu,
    ram_percent,
    disk_percent,
    network_mb_s,
    temperature,
    process_count
):
    """
    Convert raw metric values into
    ML feature vector.
    """
    features = np.array([
        cpu,
        ram_percent,
        disk_percent,
        network_mb_s,
        temperature,
        process_count
    ]).reshape(1, -1)

    return features

# -------------------------------
# Predict Failure
# -------------------------------
def predict_failure(features):
    """
    Predict system failure risk.
    """
    model = load_model()

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(features)
        failure_probability = round(probabilities[0][1] * 100, 2)
        confidence = round(max(probabilities[0]) * 100, 2)
    else:
        prediction = model.predict(features)
        failure_probability = 100 if prediction[0] == 1 else 0
        confidence = 100

    result = {
        "failure_probability": failure_probability,
        "confidence": confidence,
        "high_risk": failure_probability >= 70
    }

    logger.info(
        f"Prediction Result | Failure Probability: "
        f"{failure_probability}% | Confidence: {confidence}%"
    )

    return result

# -------------------------------
# CLI Interface
# -------------------------------
def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Predict system failure risk"
    )

    parser.add_argument("--cpu", type=float, required=True)
    parser.add_argument("--ram", type=float, required=True)
    parser.add_argument("--disk", type=float, required=True)
    parser.add_argument("--network", type=float, required=True)
    parser.add_argument("--temp", type=float, required=True)
    parser.add_argument("--processes", type=int, required=True)

    return parser.parse_args()

# -------------------------------
# Main
# -------------------------------
def main():
    args = parse_args()

    features = prepare_features(
        cpu=args.cpu,
        ram_percent=args.ram,
        disk_percent=args.disk,
        network_mb_s=args.network,
        temperature=args.temp,
        process_count=args.processes
    )

    result = predict_failure(features)

    print("\n===== SYSTEM FAILURE PREDICTION =====")
    print(f"Failure Probability : {result['failure_probability']}%")
    print(f"Prediction Confidence: {result['confidence']}%")
    print(
        "Risk Level           : "
        + ("HIGH ⚠️" if result["high_risk"] else "LOW ✅")
    )
    print("=====================================\n")

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    main()

# -------------------------------
# End of predict_failure.py
# -------------------------------
