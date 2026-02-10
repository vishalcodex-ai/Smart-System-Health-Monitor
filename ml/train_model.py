# ==========================================
# File: train_model.py
# Project: Smart System Health Monitor
# Description:
#   Trains a Machine Learning model to
#   predict future system failure risk
#   based on historical system metrics.
#   Saves trained model to model.pkl
# ==========================================

import os
import pickle
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from config.paths import (
    SYSTEM_LOG_FILE,
    PREDICTION_DATA_FILE,
    ML_MODEL_FILE
)

from utils.logger import get_logger

# -------------------------------
# Initialize Logger
# -------------------------------
logger = get_logger(__name__)

# -------------------------------
# Load Dataset
# -------------------------------
def load_dataset():
    """
    Load and merge system logs & prediction data.
    """
    if not os.path.exists(SYSTEM_LOG_FILE):
        raise FileNotFoundError("System log data not found")

    system_df = pd.read_csv(SYSTEM_LOG_FILE)

    # If prediction data exists, merge (optional)
    if os.path.exists(PREDICTION_DATA_FILE):
        pred_df = pd.read_csv(PREDICTION_DATA_FILE)
        df = system_df.merge(
            pred_df,
            on="timestamp",
            how="left"
        )
    else:
        df = system_df

    logger.info(f"Dataset loaded with {len(df)} records")
    return df

# -------------------------------
# Preprocess Data
# -------------------------------
def preprocess_data(df):
    """
    Clean and prepare features & labels.
    """
    # Fill missing values
    df.fillna(0, inplace=True)

    feature_cols = [
        "cpu",
        "ram_percent",
        "disk_percent",
        "network_mb_s",
        "temperature",
        "process_count"
    ]

    X = df[feature_cols]

    # Label creation (rule-based)
    # Failure = 1 if extreme conditions observed
    y = (
        (df["cpu"] > 90) |
        (df["ram_percent"] > 90) |
        (df["disk_percent"] > 95) |
        (df["temperature"] > 85)
    ).astype(int)

    logger.info("Data preprocessing completed")
    return X, y

# -------------------------------
# Train Model
# -------------------------------
def train_model(X, y):
    """
    Train RandomForest classifier.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    logger.info(f"Model accuracy: {accuracy * 100:.2f}%")
    logger.info("Classification Report:")
    logger.info("\n" + classification_report(y_test, y_pred))

    return model

# -------------------------------
# Save Model
# -------------------------------
def save_model(model):
    """
    Save trained model to disk.
    """
    os.makedirs(os.path.dirname(ML_MODEL_FILE), exist_ok=True)

    with open(ML_MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

    logger.info(f"Model saved to {ML_MODEL_FILE}")

# -------------------------------
# Main Training Pipeline
# -------------------------------
def main():
    try:
        logger.info("ML training started")

        df = load_dataset()
        X, y = preprocess_data(df)
        model = train_model(X, y)
        save_model(model)

        logger.info("ML training completed successfully")

    except Exception as e:
        logger.error(f"Training failed: {e}")

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    main()

# -------------------------------
# End of train_model.py
# -------------------------------
