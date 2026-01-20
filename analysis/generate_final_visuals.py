#!/usr/bin/env python3
"""
Generate Final High-Impact Visualizations for UIDAI Hackathon Submission
- India State-Level BLI Map
- Time-Series Forecasting
- Executive Dashboard
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

print("=" * 60)
print("🚀 GENERATING FINAL HIGH-IMPACT VISUALIZATIONS")
print("=" * 60)

# Define paths
BASE_DIR = Path("/home/ayush/Projects/UDH - FInal Draft")
DATA_DIR = BASE_DIR
ANALYSIS_DIR = BASE_DIR / "uidai-bli-analyzer" / "analysis"

# Define small constant for division
epsilon = 1e-10

# Define risk level function
def get_risk_level(bli):
    if bli < 0.1:
        return 'Low'
    elif bli < 0.3:
        return 'Medium'
    elif bli < 0.5:
        return 'High'
    else:
        return 'Critical'

# Load data
print("\n📁 Loading data...")

# Load Enrollment data
enr_files = [
    DATA_DIR / "api_data_aadhar_enrolment" / f
    for f in [
        "api_data_aadhar_enrolment_0_500000.csv",
        "api_data_aadhar_enrolment_500000_1000000.csv",
        "api_data_aadhar_enrolment_1000000_1006029.csv"
    ]
]
df_enrollment = pd.concat([pd.read_csv(f) for f in enr_files], ignore_index=True)
print(f"   ✓ Enrollment: {len(df_enrollment):,} rows")

# Load Biometric data
bio_files = [
    DATA_DIR / "api_data_aadhar_biometric" / f
    for f in [
        "api_data_aadhar_biometric_0_500000.csv",
        "api_data_aadhar_biometric_500000_1000000.csv",
        "api_data_aadhar_biometric_1000000_1500000.csv",
        "api_data_aadhar_biometric_1500000_1861108.csv"
    ]
]
df_biometric = pd.concat([pd.read_csv(f) for f in bio_files], ignore_index=True)
print(f"   ✓ Biometric: {len(df_biometric):,} rows")

# Convert dates (dayfirst for DD-MM-YYYY format)
df_enrollment['date'] = pd.to_datetime(df_enrollment['date'], dayfirst=True)
df_biometric['date'] = pd.to_datetime(df_biometric['date'], dayfirst=True)

# Clean data
df_enrollment = df_enrollment.drop_duplicates()
df_biometric = df_biometric.drop_duplicates()

# Merge datasets
print("\n📊 Merging datasets...")
df_merged = df_enrollment.merge(
    df_biometric,
    on=['date', 'state', 'district', 'pincode'],
    how='outer'
).fillna(0)

# Create BLI metrics
df_merged['age_5_17'] = df_merged['age_5_17'].astype(float)
df_merged['bio_age_5_17'] = df_merged['bio_age_5_17'].astype(float)
df_merged['child_update_gap'] = df_merged['age_5_17'] - df_merged['bio_age_5_17']
df_merged['total_enrollments'] = df_merged[['age_0_5', 'age_5_17', 'age_18_greater']].sum(axis=1)

print(f"   ✓ Merged dataset: {len(df_merged):,} rows")

# =============================================================================
# VISUALIZATION 1: INDIA STATE-LEVEL BLI MAP
# =============================================================================
print("\n" + "=" * 60)
print("🗺️ GENERATING: INDIA STATE-LEVEL BLI MAP")
print("=" * 60)

# Prepare state-level data
state_bli = df_merged.groupby('state').agg({
    'age_5_17': 'sum',
    'bio_age_5_17': 'sum',
    'child_update_gap': 'sum',
    'total_enrollments': 'sum',
    'district': 'nunique',
    'pincode': 'nunique'
}).reset_index()

state_bli['bli'] = state_bli['child_update_gap'] / (state_bli['age_5_17'] + epsilon)
state_bli = state_bli[state_bli['bli'].between(0, 1)]
state_bli['risk_level'] = state_bli['bli'].apply(get_risk_level)
state_bli['children_at_risk'] = state_bli['child_update_gap'].clip(lower=0)
state_bli['state_display'] = state_bli['state'].str.title()

print(f"\n📊 States analyzed: {len(state_bli)}")
print(f"📊 Total children at risk: {state_bli['children_at_risk'].sum():,.0f}")

# Create comprehensive state-level visualization
fig, axes = plt.subplots(2, 2, figsize=(18, 14))

# PLOT 1: Horizontal Bar Chart - BLI by State
ax1 = axes[0, 0]
state_sorted = state_bli.sort_values('bli', ascending=True)

colors = state_sorted['risk_level'].map({
    'Low': '#27ae60', 'Medium': '#f39c12', 'High': '#e67e22', 'Critical': '#c0392b'
})

bars = ax1.barh(state_sorted['state_display'], state_sorted['bli'], color=colors, edgecolor='black', linewidth=0.5)

ax1.axvline(x=0.1, color='green', linestyle='--', alpha=0.7, linewidth=2, label='Low/Medium (0.1)')
ax1.axvline(x=0.3, color='orange', linestyle='--', alpha=0.7, linewidth=2, label='Medium/High (0.3)')
ax1.axvline(x=0.5, color='red', linestyle='--', alpha=0.7, linewidth=2, label='High/Critical (0.5)')

ax1.set_xlabel('Biometric Lag Index (BLI)', fontsize=12, fontweight='bold')
ax1.set_ylabel('State', fontsize=12, fontweight='bold')
ax1.set_title('🗺️ STATE-WISE BIOMETRIC LAG INDEX\n(Sorted by BLI - Higher = More Children at Risk)', fontsize=14, fontweight='bold')
ax1.legend(loc='lower right', fontsize=9)
ax1.set_xlim(0, 1.1)

for bar, val in zip(bars, state_sorted['bli']):
    ax1.text(val + 0.02, bar.get_y() + bar.get_height()/2, f'{val:.3f}', va='center', fontsize=8, fontweight='bold')

# PLOT 2: Risk Level Distribution
ax2 = axes[0, 1]
risk_counts = state_bli['risk_level'].value_counts()
risk_order = ['Critical', 'High', 'Medium', 'Low']
risk_counts = risk_counts.reindex([r for r in risk_order if r in risk_counts.index])

colors_pie = {'Critical': '#c0392b', 'High': '#e67e22', 'Medium': '#f39c12', 'Low': '#27ae60'}
pie_colors = [colors_pie[r] for r in risk_counts.index]

wedges, texts, autotexts = ax2.pie(
    risk_counts.values, 
    labels=[f'{r}\n({v} states)' for r, v in zip(risk_counts.index, risk_counts.values)],
    autopct='%1.1f%%',
    colors=pie_colors, 
    explode=[0.1 if r == 'Critical' else 0 for r in risk_counts.index],
    shadow=True, startangle=90,
    textprops={'fontsize': 11, 'fontweight': 'bold'}
)
ax2.set_title('📊 STATE RISK LEVEL DISTRIBUTION\n(Based on BLI Score)', fontsize=14, fontweight='bold')

# PLOT 3: Children at Risk by State (Top 15)
ax3 = axes[1, 0]
top_states_risk = state_bli.nlargest(15, 'children_at_risk')

colors3 = top_states_risk['risk_level'].map({
    'Low': '#27ae60', 'Medium': '#f39c12', 'High': '#e67e22', 'Critical': '#c0392b'
})

bars3 = ax3.barh(top_states_risk['state_display'], top_states_risk['children_at_risk'], 
                  color=colors3, edgecolor='black', linewidth=0.5)

ax3.set_xlabel('Children at Risk (Update Gap)', fontsize=12, fontweight='bold')
ax3.set_ylabel('State', fontsize=12, fontweight='bold')
ax3.set_title('👶 TOP 15 STATES BY CHILDREN AT RISK\n(Absolute Number of Children with Outdated Biometrics)', fontsize=14, fontweight='bold')

for bar, val in zip(bars3, top_states_risk['children_at_risk']):
    ax3.text(val + val*0.02, bar.get_y() + bar.get_height()/2, f'{val:,.0f}', va='center', fontsize=9, fontweight='bold')

# PLOT 4: BLI vs Children at Risk Scatter
ax4 = axes[1, 1]

colors4 = state_bli['risk_level'].map({
    'Low': '#27ae60', 'Medium': '#f39c12', 'High': '#e67e22', 'Critical': '#c0392b'
})

scatter = ax4.scatter(state_bli['bli'], state_bli['children_at_risk'], 
                       c=colors4, s=state_bli['district']*5, 
                       alpha=0.7, edgecolors='black', linewidth=0.5)

for _, row in state_bli.nlargest(5, 'bli').iterrows():
    ax4.annotate(row['state_display'], (row['bli'], row['children_at_risk']),
                 xytext=(5, 5), textcoords='offset points', fontsize=8, fontweight='bold')

ax4.axvline(x=0.5, color='red', linestyle='--', alpha=0.7, linewidth=2, label='Critical Threshold')
ax4.set_xlabel('Biometric Lag Index (BLI)', fontsize=12, fontweight='bold')
ax4.set_ylabel('Children at Risk', fontsize=12, fontweight='bold')
ax4.set_title('📈 BLI vs CHILDREN AT RISK BY STATE\n(Bubble size = Number of Districts)', fontsize=14, fontweight='bold')
ax4.legend()

plt.tight_layout()
plt.savefig(ANALYSIS_DIR / 'india_state_bli_map.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("\n✅ Saved: india_state_bli_map.png")

# =============================================================================
# VISUALIZATION 2: TIME-SERIES FORECASTING
# =============================================================================
print("\n" + "=" * 60)
print("📈 GENERATING: TIME-SERIES FORECASTING")
print("=" * 60)

# Monthly aggregation
df_merged['month'] = df_merged['date'].dt.to_period('M')
monthly_data = df_merged.groupby('month').agg({
    'age_5_17': 'sum',
    'bio_age_5_17': 'sum',
    'child_update_gap': 'sum',
    'total_enrollments': 'sum'
}).reset_index()

monthly_data['bli'] = monthly_data['child_update_gap'] / (monthly_data['age_5_17'] + epsilon)
monthly_data = monthly_data[monthly_data['bli'].between(0, 1)]
monthly_data['month_num'] = range(len(monthly_data))

# Simple linear forecast
if len(monthly_data) >= 3:
    # Fit linear trend
    x = monthly_data['month_num'].values
    y = monthly_data['bli'].values
    
    # Linear regression
    coeffs = np.polyfit(x, y, 1)
    trend_line = np.poly1d(coeffs)
    
    # Forecast next 6 months
    last_month = monthly_data['month_num'].iloc[-1]
    forecast_months = np.array(range(last_month + 1, last_month + 7))
    forecast_bli = trend_line(forecast_months)
    forecast_bli = np.clip(forecast_bli, 0, 1)
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: BLI Time Series with Forecast
    ax1 = axes[0, 0]
    ax1.plot(monthly_data['month_num'], monthly_data['bli'], 'b-o', linewidth=2, markersize=8, label='Historical BLI')
    ax1.plot(monthly_data['month_num'], trend_line(monthly_data['month_num']), 'g--', linewidth=2, alpha=0.7, label='Trend Line')
    ax1.plot(forecast_months, forecast_bli, 'r--o', linewidth=2, markersize=8, label='6-Month Forecast')
    ax1.fill_between(forecast_months, forecast_bli * 0.9, forecast_bli * 1.1, alpha=0.3, color='red', label='Confidence Band')
    ax1.axhline(y=0.5, color='darkred', linestyle=':', linewidth=2, label='Critical Threshold')
    ax1.set_xlabel('Month Index', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Biometric Lag Index', fontsize=12, fontweight='bold')
    ax1.set_title('📈 BLI TREND WITH 6-MONTH FORECAST', fontsize=14, fontweight='bold')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Children at Risk Trend
    ax2 = axes[0, 1]
    children_at_risk = monthly_data['child_update_gap'].clip(lower=0)
    ax2.bar(monthly_data['month_num'], children_at_risk, color='coral', edgecolor='black', alpha=0.8)
    ax2.plot(monthly_data['month_num'], children_at_risk, 'ro-', linewidth=2)
    ax2.set_xlabel('Month Index', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Children at Risk', fontsize=12, fontweight='bold')
    ax2.set_title('👶 CHILDREN AT RISK TREND', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Enrollment vs Biometric Updates
    ax3 = axes[1, 0]
    width = 0.35
    x_pos = monthly_data['month_num'].values
    ax3.bar(x_pos - width/2, monthly_data['age_5_17'], width, label='Enrollments (5-17)', color='steelblue', alpha=0.8)
    ax3.bar(x_pos + width/2, monthly_data['bio_age_5_17'], width, label='Biometric Updates', color='seagreen', alpha=0.8)
    ax3.set_xlabel('Month Index', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax3.set_title('📊 ENROLLMENTS vs BIOMETRIC UPDATES COMPARISON', fontsize=14, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Forecast Summary
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Calculate key statistics
    current_bli = monthly_data['bli'].iloc[-1]
    forecast_final = forecast_bli[-1]
    trend_direction = "INCREASING" if coeffs[0] > 0 else "DECREASING"
    trend_color = "red" if coeffs[0] > 0 else "green"
    
    summary_text = f"""
╔════════════════════════════════════════════════════════╗
║              📊 FORECAST SUMMARY REPORT                ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  CURRENT STATE                                         ║
║  ─────────────                                         ║
║  • Current BLI: {current_bli:.4f}                           ║
║  • Risk Level: {get_risk_level(current_bli):>10}                        ║
║  • Total Children at Risk: {int(children_at_risk.iloc[-1]):,}              ║
║                                                        ║
║  TREND ANALYSIS                                        ║
║  ─────────────                                         ║
║  • Trend Direction: {trend_direction:>10}                   ║
║  • Monthly Change Rate: {coeffs[0]:.4f}                     ║
║                                                        ║
║  6-MONTH FORECAST                                      ║
║  ─────────────────                                     ║
║  • Projected BLI: {forecast_final:.4f}                      ║
║  • Projected Risk: {get_risk_level(forecast_final):>10}                    ║
║                                                        ║
║  ⚠️  KEY INSIGHTS                                      ║
║  ───────────────                                       ║
║  • If trend continues, {trend_direction.lower()} risk          ║
║  • Immediate intervention needed for Critical states   ║
║  • Focus on districts with BLI > 0.5                   ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
"""
    ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes, fontsize=11,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    ax4.set_title('📋 FORECAST INSIGHTS', fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    plt.savefig(ANALYSIS_DIR / 'forecast_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Saved: forecast_analysis.png")

# =============================================================================
# VISUALIZATION 3: EXECUTIVE DASHBOARD
# =============================================================================
print("\n" + "=" * 60)
print("📊 GENERATING: EXECUTIVE DASHBOARD")
print("=" * 60)

# Create district-level analysis
district_analysis = df_merged.groupby(['state', 'district']).agg({
    'age_5_17': 'sum',
    'bio_age_5_17': 'sum',
    'child_update_gap': 'sum',
    'total_enrollments': 'sum',
    'pincode': 'nunique'
}).reset_index()

district_analysis['bli'] = district_analysis['child_update_gap'] / (district_analysis['age_5_17'] + epsilon)
district_analysis = district_analysis[district_analysis['bli'].between(0, 1)]
district_analysis['risk_level'] = district_analysis['bli'].apply(get_risk_level)
district_analysis['children_at_risk'] = district_analysis['child_update_gap'].clip(lower=0)

# Calculate key metrics
total_children = df_merged['age_5_17'].sum()
total_at_risk = df_merged['child_update_gap'].clip(lower=0).sum()
national_bli = total_at_risk / (total_children + epsilon)
total_states = df_merged['state'].nunique()
total_districts = df_merged['district'].nunique()
total_pincodes = df_merged['pincode'].nunique()

critical_districts = len(district_analysis[district_analysis['risk_level'] == 'Critical'])
high_risk_districts = len(district_analysis[district_analysis['risk_level'] == 'High'])

# Create Executive Dashboard
fig = plt.figure(figsize=(20, 14))

# Title
fig.suptitle('🏛️ UIDAI BIOMETRIC LAG INDEX (BLI) - EXECUTIVE DASHBOARD', 
             fontsize=20, fontweight='bold', y=0.98)

# Create grid
gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

# ============================================
# KPI BOXES (Top Row)
# ============================================

# KPI 1: National BLI
ax_kpi1 = fig.add_subplot(gs[0, 0])
ax_kpi1.set_xlim(0, 1)
ax_kpi1.set_ylim(0, 1)
ax_kpi1.axis('off')
kpi_color = '#c0392b' if national_bli > 0.5 else '#f39c12' if national_bli > 0.3 else '#27ae60'
rect = mpatches.FancyBboxPatch((0.05, 0.1), 0.9, 0.8, boxstyle="round,pad=0.02", 
                                 facecolor=kpi_color, alpha=0.9, edgecolor='black', linewidth=2)
ax_kpi1.add_patch(rect)
ax_kpi1.text(0.5, 0.7, f'{national_bli:.4f}', ha='center', va='center', 
             fontsize=28, fontweight='bold', color='white')
ax_kpi1.text(0.5, 0.3, 'National BLI', ha='center', va='center', 
             fontsize=14, fontweight='bold', color='white')

# KPI 2: Children at Risk
ax_kpi2 = fig.add_subplot(gs[0, 1])
ax_kpi2.set_xlim(0, 1)
ax_kpi2.set_ylim(0, 1)
ax_kpi2.axis('off')
rect = mpatches.FancyBboxPatch((0.05, 0.1), 0.9, 0.8, boxstyle="round,pad=0.02", 
                                 facecolor='#e74c3c', alpha=0.9, edgecolor='black', linewidth=2)
ax_kpi2.add_patch(rect)
ax_kpi2.text(0.5, 0.7, f'{total_at_risk:,.0f}', ha='center', va='center', 
             fontsize=22, fontweight='bold', color='white')
ax_kpi2.text(0.5, 0.3, 'Children at Risk', ha='center', va='center', 
             fontsize=14, fontweight='bold', color='white')

# KPI 3: Critical Districts
ax_kpi3 = fig.add_subplot(gs[0, 2])
ax_kpi3.set_xlim(0, 1)
ax_kpi3.set_ylim(0, 1)
ax_kpi3.axis('off')
rect = mpatches.FancyBboxPatch((0.05, 0.1), 0.9, 0.8, boxstyle="round,pad=0.02", 
                                 facecolor='#c0392b', alpha=0.9, edgecolor='black', linewidth=2)
ax_kpi3.add_patch(rect)
ax_kpi3.text(0.5, 0.7, f'{critical_districts}', ha='center', va='center', 
             fontsize=28, fontweight='bold', color='white')
ax_kpi3.text(0.5, 0.3, 'Critical Districts', ha='center', va='center', 
             fontsize=14, fontweight='bold', color='white')

# KPI 4: Coverage
ax_kpi4 = fig.add_subplot(gs[0, 3])
ax_kpi4.set_xlim(0, 1)
ax_kpi4.set_ylim(0, 1)
ax_kpi4.axis('off')
rect = mpatches.FancyBboxPatch((0.05, 0.1), 0.9, 0.8, boxstyle="round,pad=0.02", 
                                 facecolor='#3498db', alpha=0.9, edgecolor='black', linewidth=2)
ax_kpi4.add_patch(rect)
ax_kpi4.text(0.5, 0.65, f'{total_states}', ha='center', va='center', 
             fontsize=22, fontweight='bold', color='white')
ax_kpi4.text(0.5, 0.45, f'States / {total_districts} Dist', ha='center', va='center', 
             fontsize=11, fontweight='bold', color='white')
ax_kpi4.text(0.5, 0.25, f'{total_pincodes:,} Pincodes', ha='center', va='center', 
             fontsize=11, fontweight='bold', color='white')

# ============================================
# Chart 1: Top 10 Critical Districts
# ============================================
ax1 = fig.add_subplot(gs[1, :2])
top_critical = district_analysis.nlargest(10, 'bli')
colors1 = ['#c0392b' if r == 'Critical' else '#e67e22' for r in top_critical['risk_level']]
bars1 = ax1.barh(top_critical['district'] + '\n(' + top_critical['state'].str[:15] + ')', 
                  top_critical['bli'], color=colors1, edgecolor='black')
ax1.axvline(x=0.5, color='darkred', linestyle='--', linewidth=2, label='Critical Threshold')
ax1.set_xlabel('Biometric Lag Index (BLI)', fontsize=12, fontweight='bold')
ax1.set_title('🔴 TOP 10 CRITICAL DISTRICTS (Highest BLI)', fontsize=14, fontweight='bold')
ax1.legend()
ax1.set_xlim(0, 1.1)

# ============================================
# Chart 2: Risk Distribution Pie
# ============================================
ax2 = fig.add_subplot(gs[1, 2])
risk_dist = district_analysis['risk_level'].value_counts()
risk_order = ['Critical', 'High', 'Medium', 'Low']
risk_dist = risk_dist.reindex([r for r in risk_order if r in risk_dist.index])
colors2 = ['#c0392b', '#e67e22', '#f39c12', '#27ae60'][:len(risk_dist)]
ax2.pie(risk_dist.values, labels=risk_dist.index, autopct='%1.1f%%', colors=colors2,
        explode=[0.1 if i == 0 else 0 for i in range(len(risk_dist))], shadow=True)
ax2.set_title('📊 DISTRICT RISK DISTRIBUTION', fontsize=14, fontweight='bold')

# ============================================
# Chart 3: State BLI Bar
# ============================================
ax3 = fig.add_subplot(gs[1, 3])
top_states = state_bli.nlargest(8, 'bli')
colors3 = top_states['risk_level'].map({
    'Low': '#27ae60', 'Medium': '#f39c12', 'High': '#e67e22', 'Critical': '#c0392b'
})
ax3.barh(top_states['state_display'], top_states['bli'], color=colors3, edgecolor='black')
ax3.set_xlabel('BLI', fontsize=11, fontweight='bold')
ax3.set_title('📈 TOP 8 STATES BY BLI', fontsize=14, fontweight='bold')
ax3.set_xlim(0, 1.1)

# ============================================
# Bottom Row: Recommendations
# ============================================
ax_rec = fig.add_subplot(gs[2, :])
ax_rec.axis('off')

recommendations = f"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                          🎯 STRATEGIC RECOMMENDATIONS                                                  ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                                       ║
║  🔴 IMMEDIATE ACTION (BLI > 0.5 - Critical):                                                                          ║
║     • Deploy mobile biometric update camps in {critical_districts} critical districts                                              ║
║     • Priority focus on Purbi Champaran, Bengaluru Urban, Dinajpur Uttar                                              ║
║     • Estimated {total_at_risk:,.0f} children require immediate biometric updates                                                   ║
║                                                                                                                       ║
║  🟠 SHORT-TERM (30-60 days):                                                                                          ║
║     • Scale up mobile camps to {high_risk_districts} high-risk districts (BLI 0.3-0.5)                                              ║
║     • Partner with schools for mass enrollment drives                                                                 ║
║     • SMS/WhatsApp awareness campaigns                                                                                ║
║                                                                                                                       ║
║  🟢 LONG-TERM STRATEGY:                                                                                               ║
║     • Implement real-time BLI monitoring dashboard                                                                    ║
║     • Predictive alerts for districts approaching critical threshold                                                  ║
║     • Integrate with school enrollment systems for automatic triggers                                                 ║
║                                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

                                        📅 Report Generated: January 2025 | 📊 Data Source: UIDAI API
"""

ax_rec.text(0.02, 0.9, recommendations, transform=ax_rec.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.95, edgecolor='black'))

plt.savefig(ANALYSIS_DIR / 'executive_dashboard.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Saved: executive_dashboard.png")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 60)
print("🎉 ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
print("=" * 60)
print(f"\n📁 Output directory: {ANALYSIS_DIR}")
print("\n📊 Generated files:")
print("   1. india_state_bli_map.png     - State-level BLI distribution")
print("   2. forecast_analysis.png       - Time-series forecasting")
print("   3. executive_dashboard.png     - One-page executive summary")
print("\n✅ Ready for UIDAI Hackathon Submission!")
