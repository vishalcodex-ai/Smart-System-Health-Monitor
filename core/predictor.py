# ==========================================
# File: predictor.py
# Project: Smart System Health Monitor
# Description:
#   Predicts future system failure risk using
#   Machine Learning model.
#   Uses historical metrics to estimate
#   probability of failure and confidence.
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
# System Failure Predictor Class
# -------------------------------
class FailurePredictor:
    """
    Predicts future system failure probability
    using trained ML model.
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
        """
        Load trained ML model from disk.
        """
        if not os.path.exists(ML_MODEL_PATH):
            logger.warning(
                "ML model not found. Prediction disabled."
            )
            return

        try:
            with open(ML_MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)

            self.model_loaded = True
            logger.info("ML model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")

    # -------------------------------
    # Prepare Feature Vector
    # -------------------------------
    def _prepare_features(self, analysis_result):
        """
        Convert analysis results into ML feature vector.
        """
        feature_map = {
            "cpu": 0,
            "ram": 0,
            "disk": 0,
            "network": 0,
            "temperature": 0
        }

        severity_score = {
            "normal": 0,
            "warning": 1,
            "high": 2,
            "critical": 3
        }

        for item in analysis_result:
            metric = item["metric"]
            status = item["status"]

            if metric in feature_map:
                feature_map[metric] = severity_score.get(status, 0)

        return np.array(list(feature_map.values())).reshape(1, -1)

    # -------------------------------
    # Predict Failure
    # -------------------------------
    def predict(self, analysis_result):
        """
        Predict failure probability and confidence.
        """
        if not ENABLE_ML_PREDICTION or not self.model_loaded:
            return {
                "prediction_enabled": False,
                "failure_probability": None,
                "confidence": None,
                "message": "ML prediction disabled or model not loaded"
            }

        try:
            features = self._prepare_features(analysis_result)

            # Predict probability
            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba(features)
                failure_probability = round(
                    probabilities[0][1] * 100, 2
                )
                confidence = round(
                    max(probabilities[0]) * 100, 2
                )
            else:
                prediction = self.model.predict(features)
                failure_probability = 100 if prediction[0] == 1 else 0
                confidence = 100

            result = {
                "prediction_enabled": True,
                "failure_probability": failure_probability,
                "confidence": confidence,
                "high_risk": confidence >= (
                    PREDICTION_CONFIDENCE_THRESHOLD * 100
                )
            }

            # Save prediction data
            self._save_prediction(result)

            logger.info(
                f"Failure Prediction | Probability: {failure_probability}% "
                f"| Confidence: {confidence}%"
            )

            return result

        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {
                "prediction_enabled": False,
                "failure_probability": None,
                "confidence": None,
                "message": "Prediction error"
            }

    # -------------------------------
    # Save Prediction Data
    # -------------------------------
    def _save_prediction(self, prediction_result):
        """
        Append prediction data for future training.
        """
        try:
            record = {
                "timestamp": datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "failure_probability": prediction_result["failure_probability"],
                "confidence": prediction_result["confidence"]
            }

            append_prediction_data(record)

        except Exception as e:
            logger.error(f"Failed to save prediction data: {e}")

# -------------------------------
# End of predictor.py
# -------------------------------
