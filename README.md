# 🚀 Smart System Health Monitor

An **AI-based Smart System Health Monitoring & Failure Prediction Dashboard** built using **Python, Flask, and Machine Learning**.  
This project monitors real-time system performance (CPU, RAM, Disk), detects critical health conditions, generates alerts, and predicts possible future system failures.

---

## 📌 Features

- 📊 Real-time monitoring of:
  - CPU Usage
  - RAM Usage
  - Disk Usage
- 🧠 Intelligent Health Score Calculation
- ⚠️ Smart Alert System with Cooldown (prevents false alerts)
- 🔮 Failure Prediction using Machine Learning
- 🧹 Automatic RAM Cleanup during Critical Conditions
- 🌐 Web-based Dashboard (Flask)
- ☁️ Cloud-ready (Railway / Render)

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Backend Framework:** Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **Machine Learning:** Scikit-learn  
- **System Monitoring:** psutil  
- **Version Control:** Git & GitHub  

---

## 📂 Project Structure

Smart-System-Health-Monitor/<br>
│
├── core/ # Core system logic (monitoring, analysis, prediction)<br>
├── dashboard/ # Flask dashboard (UI + APIs)<br>
│ ├── templates/<br>
│ ├── static/<br>
│ └── app.py<br>
├── ml/ # Machine learning training & prediction<br>
├── utils/ # Utility helpers (logging, scoring, file handling)<br>
├── config/ # Configuration & thresholds<br>
├── tests/ # Unit tests<br>
├── docs/ # Viva & documentation files<br>
├── requirements.txt # Project dependencies<br>
├── main.py # Project entry point<br>
└── README.md<br>

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/vishalcodex-ai/Smart-System-Health-Monitor.git
cd Smart-System-Health-Monitor


## 📸 Screenshots

### Dashboard View
![Dashboard](screenshots/dashboard.png)

### Alert Notification
![Alert](screenshots/alert.png)

### Failure Prediction
![Prediction](screenshots/prediction.png)
