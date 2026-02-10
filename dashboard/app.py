# ==========================================
# File: dashboard/app.py
# Project: Smart System Health Monitor
# Cloud Ready (Railway / Render)
# ==========================================

import os
import sys
import threading
import time
from flask import Flask, render_template, jsonify

# -------------------------------
# Fix Python Path
# -------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# -------------------------------
# Project Imports
# -------------------------------
from core.monitor import SystemMonitor
from core.analyzer import SystemAnalyzer
from core.predictor import FailurePredictor
from core.auto_cleaner import auto_clean_ram
from utils.file_handler import append_system_log
from utils.logger import get_logger

# -------------------------------
# Flask App
# -------------------------------
app = Flask(__name__)
logger = get_logger("dashboard")

# -------------------------------
# Core Components
# -------------------------------
monitor = SystemMonitor()
analyzer = SystemAnalyzer()
predictor = FailurePredictor()

# -------------------------------
# Shared State
# -------------------------------
latest_metrics = {}
latest_analysis = {}
latest_prediction = {}

# -------------------------------
# ALERT CONTROL (🔥 NEW)
# -------------------------------
LAST_ALERT_TIME = 0
ALERT_COOLDOWN = 300  # 5 minutes

# -------------------------------
# SMART HEALTH ENGINE
# -------------------------------
def enrich_analysis(metrics, analysis):
    global LAST_ALERT_TIME

    cpu = metrics.get("cpu", 0)
    ram = metrics.get("ram", {}).get("percent", 0)
    disk = metrics.get("disk", {}).get("percent", 0)

    problems = []
    reasons = []
    suggestions = []

    score = 100

    # ---------- CPU ----------
    if cpu > 85:
        score -= 40
        problems.append("CPU Overloaded")
        reasons.append("Too many heavy processes running")
        suggestions.append("Background processes band karo")

    # ---------- RAM ----------
    if ram > 90:
        score -= 40
        problems.append("RAM Almost Full")
        reasons.append("Memory heavy apps chal rahi hain")
        suggestions.append("System restart ya startup apps kam karo")

    # ---------- DISK ----------
    if disk > 85:
        score -= 20
        problems.append("Disk Usage High")
        reasons.append("Disk space kam hai")
        suggestions.append("Unused files delete karo")

    # ---------- ALERT LOGIC ----------
    current_time = time.time()
    show_alert = False

    if score <= 40:
        status = "Critical"

        if current_time - LAST_ALERT_TIME > ALERT_COOLDOWN:
            show_alert = True
            LAST_ALERT_TIME = current_time

        message = "⚠️ High risk: system crash ho sakta hai"

    elif score <= 70:
        status = "Warning"
        message = "⚠️ System pressure me hai"
    else:
        status = "Healthy"
        message = "✅ System healthy hai"

    analysis["health"] = {
        "score": max(score, 0),
        "status": status,
        "message": message,
        "problems": problems,
        "reasons": reasons,
        "suggestions": suggestions,
        "show_alert": show_alert   # 🔥 IMPORTANT
    }

    return analysis

# -------------------------------
# Background Monitor Thread
# -------------------------------
def background_monitor():
    logger.info("Background monitoring started")

    global latest_metrics, latest_analysis, latest_prediction

    while True:
        try:
            metrics = monitor.collect_metrics()
            append_system_log(metrics)

            analysis = analyzer.analyze_metrics(metrics)
            analysis = enrich_analysis(metrics, analysis)

            # Auto clean only when alert is real
            if analysis["health"]["status"] == "Critical" and analysis["health"]["show_alert"]:
                auto_clean_ram()

            prediction = predictor.predict(analysis.get("analysis", {}))

            latest_metrics = metrics
            latest_analysis = analysis
            latest_prediction = prediction

        except Exception as e:
            logger.error(f"Background error: {e}")

        time.sleep(5)

# -------------------------------
# Start Background Thread
# -------------------------------
threading.Thread(
    target=background_monitor,
    daemon=True
).start()

# -------------------------------
# Routes
# -------------------------------
@app.route("/")
def index():
    return render_template(
        "index.html",
        metrics=latest_metrics,
        analysis=latest_analysis,
        prediction=latest_prediction
    )

@app.route("/alerts")
def alerts():
    return render_template("alerts.html", analysis=latest_analysis)

@app.route("/prediction")
def prediction_page():
    return render_template("prediction.html", prediction=latest_prediction)

# -------------------------------
# API Routes
# -------------------------------
@app.route("/api/metrics")
def api_metrics():
    return jsonify(latest_metrics)

@app.route("/api/analysis")
def api_analysis():
    return jsonify(latest_analysis)

@app.route("/api/prediction")
def api_prediction():
    return jsonify(latest_prediction)

# -------------------------------
# Entry Point
# -------------------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
