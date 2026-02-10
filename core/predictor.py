# ==========================================
# File: predictor.py
# Project: Smart System Health Monitor
# Description:
#   Hybrid Failure Predictor
#   - Uses ML model if available
#   - Falls back to rule-based prediction
# ==========================================

import os
import pickle
import datetime
import numpy as np

from config.settings import (
    ENABLE_ML_PREDICTION,
    ML_MODEL_PATH,
    PREDICTION_CONFIDENCE_THRESHOLD
)

from utils.logger import get_logger
from utils.file_handler import append_prediction_data

# -------------------------------
# Initialize Logger
# -------------------------------
logger = get_logger(__name__)

# -------------------------------
# Failure Predictor
# -------------------------------
class FailurePredictor:
    """
    Predicts system failure probability using:
    - ML model (if available)
    - Rule-based fallback (always available)
    """

    def __init__(self):
        self.model = None
        self.model_loaded = False

        if ENABLE_ML_PREDICTION:
            self._load_model()

    # -------------------------------
    # Load ML Model
    # -------------------------------
    def _load_model(self):
        if not os.path.exists(ML_MODEL_PATH):
            logger.warning("ML model not found. Using rule-based prediction.")
            return

        try:
            with open(ML_MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)

            self.model_loaded = True
            logger.info("ML model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")

    # -------------------------------
    # Prepare ML Feature Vector
    # -------------------------------
    def _prepare_features(self, analysis):
        """
        Convert analysis dict into ML feature vector
        """
        cpu = analysis.get("cpu", 0)
        ram = analysis.get("ram", 0)
        disk = analysis.get("disk", 0)

        return np.array([[cpu, ram, disk]])

    # -------------------------------
    # Rule-based Prediction (Fallback)
    # -------------------------------
    def _rule_based_prediction(self, analysis):
        cpu = analysis.get("cpu", 0)
        ram = analysis.get("ram", 0)
        disk = analysis.get("disk", 0)

        risk = 0

        if cpu > 85:
            risk += 40
        elif cpu > 70:
            risk += 20

        if ram > 90:
            risk += 40
        elif ram > 75:
            risk += 20

        if disk > 85:
            risk += 20

        risk = min(risk, 100)
        confidence = round(60 + (risk / 4), 2)

        return {
            "prediction_enabled": True,
            "mode": "rule_based",
            "failure_probability": risk,
            "confidence": confidence,
            "high_risk": risk >= (PREDICTION_CONFIDENCE_THRESHOLD * 100),
            "message": "Rule-based failure prediction active"
        }

    # -------------------------------
    # Predict Failure
    # -------------------------------
    def predict(self, analysis):
        """
        Predict failure probability & confidence
        """
        # ---------- ML PATH ----------
        if ENABLE_ML_PREDICTION and self.model_loaded:
            try:
                features = self._prepare_features(analysis)

                if hasattr(self.model, "predict_proba"):
                    probabilities = self.model.predict_proba(features)
                    failure_probability = round(probabilities[0][1] * 100, 2)
                    confidence = round(max(probabilities[0]) * 100, 2)
                else:
                    prediction = self.model.predict(features)
                    failure_probability = 100 if prediction[0] == 1 else 0
                    confidence = 100

                result = {
                    "prediction_enabled": True,
                    "mode": "ml",
                    "failure_probability": failure_probability,
                    "confidence": confidence,
                    "high_risk": confidence >= (
                        PREDICTION_CONFIDENCE_THRESHOLD * 100
                    ),
                    "message": "ML-based failure prediction"
                }

                self._save_prediction(result)
                return result

            except Exception as e:
                logger.error(f"ML prediction failed: {e}")

        # ---------- FALLBACK ----------
        result = self._rule_based_prediction(analysis)
        self._save_prediction(result)
        return result

    # -------------------------------
    # Save Prediction Data
    # -------------------------------
    def _save_prediction(self, prediction):
        try:
            record = {
                "timestamp": datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "mode": prediction.get("mode"),
                "failure_probability": prediction.get("failure_probability"),
                "confidence": prediction.get("confidence")
            }

            append_prediction_data(record)

        except Exception as e:
            logger.error(f"Failed to save prediction data: {e}")

# -------------------------------
# End of predictor.py
# -------------------------------
