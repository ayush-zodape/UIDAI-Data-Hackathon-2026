# UIDAI Data Hackathon 2026 - Biometric Lag Index (BLI) Analysis

## 🏆 Competition Entry: Identifying At-Risk Child Cohorts

This submission analyzes **4.9 million Aadhaar records** to identify districts where children (ages 5-17) have enrolled but haven't updated their biometrics, creating a "Biometric Lag" that puts them at risk of service denial.

---

## 📁 Submission Contents

```
uidai-bli-analyzer/
├── README.md                           # This file
├── analysis/
│   ├── UIDAI_Comprehensive_Analysis.ipynb   # Main Analysis Notebook (66 cells)
│   ├── exports/                        # Data exports
│   │   ├── state_level_summary.csv
│   │   ├── district_level_details.csv
│   │   ├── priority_districts.csv
│   │   ├── anomalous_districts.csv
│   │   ├── district_clusters.csv
│   │   └── key_statistics.json
│   ├── *.png                           # 22 Publication-ready visualizations
│   └── *.html                          # 5 Interactive dashboards
└── .gitignore
```

---

## 🧮 BLI Formula

**BLI = (Enrollments₅₋₁₇ - BiometricUpdates₅₋₁₇) / Enrollments₅₋₁₇**

### Risk Classification
| BLI Range | Risk Level | Action Required |
|-----------|------------|-----------------|
| < 0.1 | 🟢 Low | Routine monitoring |
| 0.1 - 0.3 | 🟡 Medium | Enhanced outreach |
| 0.3 - 0.5 | 🟠 High | Priority intervention |
| > 0.5 | 🔴 Critical | Immediate action |

---

## 📊 Key Findings

| Metric | Value |
|--------|-------|
| Total Records Analyzed | 4,938,837 |
| Merged Dataset | 2,026,709 records |
| States/UTs Covered | 52 |
| Districts Analyzed | 113 |
| Critical Risk Districts | 66 (58.4%) |
| Children at Risk | 84,826 |
| Estimated Impact | ₹1,220 Lakhs in prevented service denial |

---

## 🔬 Analysis Performed

| Analysis Type | Description |
|---------------|-------------|
| ✅ Univariate | Distributions, outliers, central tendency |
| ✅ Bivariate | Correlations, scatter plots, regression |
| ✅ Trivariate | 3D visualizations, heatmaps, bubble charts |
| ✅ Geographic | State and district-level mapping |
| ✅ Clustering | K-Means (4 risk clusters, Silhouette=0.65) |
| ✅ Anomaly Detection | Isolation Forest |
| ✅ Regression | Random Forest (R²=0.91) |
| ✅ Time Series | 9-month historical + 6-month forecast |

---

## 📈 Visualizations Generated

### Static (PNG) - 22 files
- Enrollment distributions
- BLI boxplots by state
- Correlation matrices
- Geographic heatmaps
- Clustering results
- Executive dashboard

### Interactive (HTML) - 5 files
- 3D scatter plots
- Treemap
- Sankey diagram
- Radar charts
- Bubble charts

---

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- Jupyter Notebook
- Required packages: pandas, numpy, matplotlib, seaborn, plotly, scikit-learn, scipy

### Execution
1. Open `analysis/UIDAI_Comprehensive_Analysis.ipynb` in Jupyter
2. Run all cells sequentially (takes ~5-10 minutes)
3. Outputs are saved automatically to `analysis/` folder

---

## 📋 Policy Recommendations

1. **IMMEDIATE (0-30 days)**: Deploy mobile camps in top 20 critical districts
2. **SHORT-TERM (1-3 months)**: Monthly BLI monitoring dashboard
3. **LONG-TERM (3-6 months)**: State-level BLI accountability system

---

## 👤 Author

**UIDAI Data Hackathon 2026 Submission**  
January 2026

---

*This analysis was conducted using official UIDAI datasets for the Data Hackathon 2026 competition.*
