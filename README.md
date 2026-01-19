# UIDAI BLI Analyzer - Digital Continuity Platform

## Biometric Lag Index Analysis for Identifying At-Risk Cohorts

This prototype identifies districts where children (ages 5-17) have enrolled in Aadhaar but haven't updated their biometrics, creating a "Silent Gap" that puts them at risk of service disruption.

## 🚀 Quick Start

### Prerequisites
- Node.js >= 18.0.0
- Python >= 3.10
- npm >= 9.0.0

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file and add your OpenAI API key (optional for chatbot)
cp .env.example .env

# Start the server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Access the Application
- Frontend: http://localhost:5173
- Backend API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 📊 Features

1. **CSV Upload**: Drag-and-drop upload for Enrollment and Biometric data files
2. **BLI Calculation**: Automatic computation of Biometric Lag Index per district
3. **Dashboard**: Top 10 problem districts with risk levels
4. **Visualizations**: 
   - Gap Widening Curve
   - BLI Distribution Chart
   - Seasonality Analysis
5. **AI Chatbot**: Natural language queries about the data

## 📁 Data Format

### Enrollment CSV
```
date, state, district, pincode, age_0_5, age_5_17, age_18_greater
```

### Biometric Updates CSV
```
date, state, district, pincode, bio_age_5_17, bio_age_17_
```

## 🧮 BLI Formula

```
BLI = (Total Enrollments₅₋₁₇ - Total Biometric Updates₅₋₁₇) / Total Enrollments₅₋₁₇
```

### Risk Levels
| BLI Value | Risk Level | Action |
|-----------|------------|--------|
| < 0.1 | Low (Green) | Monitor |
| 0.1 - 0.3 | Medium (Yellow) | Review |
| 0.3 - 0.5 | High (Orange) | Plan Intervention |
| > 0.5 | Critical (Red) | Immediate Camp |

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

## 📝 License

Built for UIDAI Hackathon 2026 - Digital Continuity Project
