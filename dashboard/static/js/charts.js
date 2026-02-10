/* ==========================================
   File: charts.js
   Project: Smart System Health Monitor
   Description:
     Handles live fetching of system metrics,
     analysis, and prediction data from
     backend APIs.
     Designed to be chart-ready (Chart.js /
     ApexCharts can be plugged easily).
   ========================================== */

// -------------------------------
// Configuration
// -------------------------------
const REFRESH_INTERVAL_MS = 5000;

// -------------------------------
// API Endpoints
// -------------------------------
const API_ENDPOINTS = {
    metrics: "/api/metrics",
    analysis: "/api/analysis",
    prediction: "/api/prediction"
};

// -------------------------------
// Global State
// -------------------------------
let systemMetrics = {};
let systemAnalysis = {};
let systemPrediction = {};

// -------------------------------
// Fetch Helper
// -------------------------------
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("Network response not ok");
        }
        return await response.json();
    } catch (error) {
        console.error("Fetch error:", error);
        return null;
    }
}

// -------------------------------
// Update Metrics
// -------------------------------
async function updateMetrics() {
    const data = await fetchData(API_ENDPOINTS.metrics);
    if (!data) return;

    systemMetrics = data;
    console.log("Metrics updated:", systemMetrics);

    // Hook for future charts
    updateMetricCharts(systemMetrics);
}

// -------------------------------
// Update Analysis
// -------------------------------
async function updateAnalysis() {
    const data = await fetchData(API_ENDPOINTS.analysis);
    if (!data) return;

    systemAnalysis = data;
    console.log("Analysis updated:", systemAnalysis);

    // Hook for future charts
    updateAnalysisCharts(systemAnalysis);
}

// -------------------------------
// Update Prediction
// -------------------------------
async function updatePrediction() {
    const data = await fetchData(API_ENDPOINTS.prediction);
    if (!data) return;

    systemPrediction = data;
    console.log("Prediction updated:", systemPrediction);

    // Hook for future charts
    updatePredictionCharts(systemPrediction);
}

// -------------------------------
// Combined Refresh
// -------------------------------
async function refreshAll() {
    await Promise.all([
        updateMetrics(),
        updateAnalysis(),
        updatePrediction()
    ]);
}

// -------------------------------
// Chart Hooks (Placeholders)
// -------------------------------
function updateMetricCharts(metrics) {
    /*
      Example future use:
      cpuChart.update(metrics.cpu)
      ramChart.update(metrics.ram.percent)
    */
}

function updateAnalysisCharts(analysis) {
    /*
      Example future use:
      healthScoreChart.update(analysis.health_score)
    */
}

function updatePredictionCharts(prediction) {
    /*
      Example future use:
      failureRiskChart.update(prediction.failure_probability)
    */
}

// -------------------------------
// Auto Refresh Loop
// -------------------------------
function startAutoRefresh() {
    console.log("Starting dashboard auto-refresh...");
    refreshAll();
    setInterval(refreshAll, REFRESH_INTERVAL_MS);
}

// -------------------------------
// Init on Page Load
// -------------------------------
document.addEventListener("DOMContentLoaded", () => {
    startAutoRefresh();
});

// -------------------------------
// End of charts.js
// -------------------------------
