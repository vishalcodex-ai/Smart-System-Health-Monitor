# ==========================================
# Smart System Health Monitor
# Streamlit Dashboard (Railway Ready)
# ==========================================

import os
import sys
import time
import threading
import streamlit as st

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
# Streamlit Page Config (🔥 IMPORTANT)
# -------------------------------
st.set_page_config(
    page_title="Smart System Health Monitor",
    layout="wide"
)

st.title("🖥️ Smart System Health Monitor")
st.caption("Real-time system monitoring & failure prediction")

logger = get_logger("dashboard")

# -------------------------------
# Core Components
# -------------------------------
monitor = SystemMonitor()
analyzer = SystemAnalyzer()
predictor = FailurePredictor()

# -------------------------------
# Session State (IMPORTANT)
# -------------------------------
if "metrics" not in st.session_state:
    st.session_state.metrics = {}

if "analysis" not in st.session_state:
    st.session_state.analysis = {}

if "prediction" not in st.session_state:
    st.session_state.prediction = {}

# -------------------------------
# ALERT CONTROL
# -------------------------------
LAST_ALERT_TIME = 0
ALERT_COOLDOWN = 300  # seconds

# -------------------------------
# Health Enrichment Logic
# -------------------------------
def enrich_analysis(metrics, analysis):
    global LAST_ALERT_TIME

    cpu = metrics.get("cpu", 0)
    ram = metrics.get("ram", {}).get("percent", 0)
    disk = metrics.get("disk", {}).get("percent", 0)

    score = 100
    problems, reasons, suggestions = [], [], []

    if cpu > 85:
        score -= 40
        problems.append("CPU Overloaded")
        reasons.append("Heavy background processes")
        suggestions.append("Close unused applications")

    if ram > 90:
        score -= 40
        problems.append("RAM Almost Full")
        reasons.append("Memory intensive apps")
        suggestions.append("Restart system / reduce startup apps")

    if disk > 85:
        score -= 20
        problems.append("Disk Usage High")
        reasons.append("Low free disk space")
        suggestions.append("Delete unused files")

    current_time = time.time()
    show_alert = False

    if score <= 40:
        status = "Critical"
        message = "⚠️ High risk of system failure"

        if current_time - LAST_ALERT_TIME > ALERT_COOLDOWN:
            show_alert = True
            LAST_ALERT_TIME = current_time

    elif score <= 70:
        status = "Warning"
        message = "⚠️ System under pressure"
    else:
        status = "Healthy"
        message = "✅ System is healthy"

    analysis["health"] = {
        "score": max(score, 0),
        "status": status,
        "message": message,
        "problems": problems,
        "reasons": reasons,
        "suggestions": suggestions,
        "show_alert": show_alert
    }

    return analysis

# -------------------------------
# Background Monitor Thread
# -------------------------------
def background_monitor():
    logger.info("Background monitoring started")

    while True:
        try:
            metrics = monitor.collect_metrics()
            append_system_log(metrics)

            analysis = analyzer.analyze_metrics(metrics)
            analysis = enrich_analysis(metrics, analysis)

            if analysis["health"]["status"] == "Critical" and analysis["health"]["show_alert"]:
                auto_clean_ram()

            prediction = predictor.predict(analysis.get("analysis", {}))

            st.session_state.metrics = metrics
            st.session_state.analysis = analysis
            st.session_state.prediction = prediction

        except Exception as e:
            logger.error(f"Monitoring error: {e}")

        time.sleep(5)

# -------------------------------
# Start Thread Only Once
# -------------------------------
if "thread_started" not in st.session_state:
    threading.Thread(target=background_monitor, daemon=True).start()
    st.session_state.thread_started = True

# -------------------------------
# DASHBOARD UI
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "CPU Usage (%)",
        st.session_state.metrics.get("cpu", 0)
    )

with col2:
    st.metric(
        "RAM Usage (%)",
        st.session_state.metrics.get("ram", {}).get("percent", 0)
    )

with col3:
    st.metric(
        "Disk Usage (%)",
        st.session_state.metrics.get("disk", {}).get("percent", 0)
    )

st.divider()

health = st.session_state.analysis.get("health", {})

if health:
    st.subheader("🩺 System Health")

    st.progress(health.get("score", 0) / 100)

    if health["status"] == "Critical":
        st.error(health["message"])
    elif health["status"] == "Warning":
        st.warning(health["message"])
    else:
        st.success(health["message"])

    if health.get("problems"):
        st.subheader("⚠️ Problems")
        for p in health["problems"]:
            st.write("•", p)

    if health.get("suggestions"):
        st.subheader("💡 Suggestions")
        for s in health["suggestions"]:
            st.write("•", s)

st.divider()

st.subheader("🔮 Failure Prediction")
st.json(st.session_state.prediction)

st.success("Dashboard loaded successfully 🎉")
