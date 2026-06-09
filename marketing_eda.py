"""
SkillCraft Technology — Task 04
Business Insights Report: EDA on Marketing Campaign Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 1. LOAD DATASET
# ─────────────────────────────────────────────
df = pd.read_csv("marketing_campaign.csv")

print("=" * 55)
print("STEP 1 — DATASET LOADED")
print("=" * 55)
print(f"Shape      : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Columns    : {list(df.columns)}\n")

# ─────────────────────────────────────────────
# 2. DATA CLEANING
# ─────────────────────────────────────────────
print("=" * 55)
print("STEP 2 — DATA CLEANING")
print("=" * 55)
print(f"Missing values before: {df.isnull().sum().sum()}")
df['Conversions'].fillna(df['Conversions'].median(), inplace=True)
df['Revenue'].fillna(df['Revenue'].median(), inplace=True)
print(f"Missing values after : {df.isnull().sum().sum()}")

# ─────────────────────────────────────────────
# 3. FEATURE ENGINEERING
# ─────────────────────────────────────────────
df['ROI']                 = ((df['Revenue'] - df['Cost']) / df['Cost'] * 100).round(2)
df['CTR']                 = (df['Clicks'] / df['Impressions'] * 100).round(2)
df['Conv_Rate']           = (df['Conversions'] / df['Clicks'] * 100).round(2)
df['Cost_Per_Conversion'] = (df['Cost'] / df['Conversions'].replace(0, 1)).round(2)

# ─────────────────────────────────────────────
# 4. CHANNEL SUMMARY
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("STEP 3 — CHANNEL PERFORMANCE SUMMARY")
print("=" * 55)
ch = df.groupby('Channel').agg(
    Total_Cost=('Cost', 'sum'),
    Total_Revenue=('Revenue', 'sum'),
    Total_Conversions=('Conversions', 'sum'),
    Avg_CTR=('CTR', 'mean'),
    Campaigns=('Campaign_ID', 'count')
).round(2).reset_index()
ch['ROI_pct'] = ((ch['Total_Revenue'] - ch['Total_Cost']) / ch['Total_Cost'] * 100).round(1)
ch = ch.sort_values('ROI_pct', ascending=False)
print(ch[['Channel', 'Total_Cost', 'Total_Revenue', 'ROI_pct', 'Total_Conversions']].to_string(index=False))

# ─────────────────────────────────────────────
# 5. VISUALIZATION DASHBOARD
# ─────────────────────────────────────────────
colors = {
    'Email': '#2E86AB', 'Social Media': '#A23B72', 'SEO': '#F18F01',
    'PPC': '#C73E1D', 'Influencer': '#3B1F2B', 'TV Ad': '#44BBA4'
}
ch_colors = [colors[c] for c in ch['Channel']]

fig = plt.figure(figsize=(20, 14), facecolor='#F8F9FA')
fig.suptitle('Marketing Campaign EDA — Business Insights Dashboard',
             fontsize=20, fontweight='bold', y=0.98, color='#1a1a2e')
gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

# Chart 1 — ROI by Channel
ax1 = fig.add_subplot(gs[0, :2])
bars = ax1.bar(ch['Channel'], ch['ROI_pct'], color=ch_colors, edgecolor='white')
ax1.set_title('ROI % by Marketing Channel', fontweight='bold', fontsize=13)
ax1.set_ylabel('ROI (%)')
ax1.axhline(ch['ROI_pct'].mean(), color='red', linestyle='--', linewidth=1.5,
            label=f"Avg ROI: {ch['ROI_pct'].mean():.0f}%")
for bar, val in zip(bars, ch['ROI_pct']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'{val:.0f}%', ha='center', fontsize=10, fontweight='bold')
ax1.legend(); ax1.set_facecolor('#FFFFFF'); ax1.grid(axis='y', alpha=0.3)

# Chart 2 — Revenue Share
ax2 = fig.add_subplot(gs[0, 2])
ax2.pie(ch['Total_Revenue'], labels=ch['Channel'], autopct='%1.1f%%',
        colors=ch_colors, startangle=90, textprops={'fontsize': 8})
ax2.set_title('Revenue Share by Channel', fontweight='bold', fontsize=13)

# Chart 3 — Cost vs Revenue
ax3 = fig.add_subplot(gs[1, :2])
for _, row in ch.iterrows():
    ax3.scatter(row['Total_Cost'], row['Total_Revenue'],
                s=row['Total_Conversions']/5, color=colors[row['Channel']],
                alpha=0.8, edgecolors='white', linewidth=1, label=row['Channel'])
    ax3.annotate(row['Channel'], (row['Total_Cost'], row['Total_Revenue']),
                 textcoords='offset points', xytext=(5, 5), fontsize=9)
ax3.set_xlabel('Total Cost ($)'); ax3.set_ylabel('Total Revenue ($)')
ax3.set_title('Cost vs Revenue (bubble = conversions)', fontweight='bold', fontsize=13)
mn = min(ch['Total_Cost'].min(), ch['Total_Revenue'].min())
mx = max(ch['Total_Cost'].max(), ch['Total_Revenue'].max())
ax3.plot([mn, mx], [mn, mx], 'k--', alpha=0.3, label='Break-even')
ax3.legend(fontsize=8); ax3.set_facecolor('#FFFFFF'); ax3.grid(alpha=0.3)

# Chart 4 — Conversions by Region
ax4 = fig.add_subplot(gs[1, 2])
reg = df.groupby('Region')['Conversions'].sum().sort_values(ascending=True)
ax4.barh(reg.index, reg.values, color=['#2E86AB', '#A23B72', '#F18F01', '#44BBA4'])
ax4.set_title('Total Conversions\nby Region', fontweight='bold', fontsize=13)
ax4.set_xlabel('Conversions'); ax4.set_facecolor('#FFFFFF'); ax4.grid(axis='x', alpha=0.3)

# Chart 5 — Marketing Funnel
ax5 = fig.add_subplot(gs[2, 0])
funnel_vals = [df['Impressions'].sum(), df['Clicks'].sum(), int(df['Conversions'].sum())]
funnel_labels = [f"Impressions\n{funnel_vals[0]:,.0f}",
                 f"Clicks\n{funnel_vals[1]:,.0f}",
                 f"Conversions\n{funnel_vals[2]:,.0f}"]
widths = [1.0, funnel_vals[1]/funnel_vals[0], funnel_vals[2]/funnel_vals[0]]
for i, (w, lbl, col) in enumerate(zip(widths, funnel_labels,
                                       ['#2E86AB', '#F18F01', '#44BBA4'])):
    ax5.barh(i, w, color=col, height=0.6)
    ax5.text(w/2, i, lbl, ha='center', va='center',
             fontsize=9, color='white', fontweight='bold')
ax5.set_xlim(0, 1.1); ax5.set_yticks([])
ax5.set_title('Marketing Funnel', fontweight='bold', fontsize=13)
ax5.set_facecolor('#FFFFFF'); ax5.set_xlabel('Relative Size')

# Chart 6 — Avg CTR by Channel
ax6 = fig.add_subplot(gs[2, 1])
ctr = df.groupby('Channel')['CTR'].mean().sort_values(ascending=False)
ax6.bar(ctr.index, ctr.values, color=[colors[c] for c in ctr.index])
ax6.set_title('Avg Click-Through Rate\nby Channel (%)', fontweight='bold', fontsize=13)
ax6.set_ylabel('CTR (%)'); ax6.set_facecolor('#FFFFFF'); ax6.grid(axis='y', alpha=0.3)
plt.setp(ax6.get_xticklabels(), rotation=30, ha='right', fontsize=8)

# Chart 7 — Monthly Revenue Trend
ax7 = fig.add_subplot(gs[2, 2])
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly = df.groupby('Month')['Revenue'].sum().reindex(month_order)
ax7.plot(month_order, monthly.values, marker='o', color='#2E86AB', linewidth=2)
ax7.fill_between(range(12), monthly.values, alpha=0.1, color='#2E86AB')
ax7.set_title('Monthly Revenue Trend', fontweight='bold', fontsize=13)
ax7.set_ylabel('Revenue ($)'); ax7.set_facecolor('#FFFFFF'); ax7.grid(alpha=0.3)
ax7.set_xticks(range(12)); ax7.set_xticklabels(month_order, rotation=45, ha='right', fontsize=7)

plt.savefig('marketing_eda_dashboard.png', dpi=150, bbox_inches='tight', facecolor='#F8F9FA')
print("\nDashboard saved: marketing_eda_dashboard.png")

# ─────────────────────────────────────────────
# 6. FINAL INSIGHTS
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("STEP 4 — KEY BUSINESS INSIGHTS")
print("=" * 55)
top = ch.iloc[0]
bottom = ch.iloc[-1]
print(f"Best channel  : {top['Channel']} (ROI: {top['ROI_pct']}%)")
print(f"Worst channel : {bottom['Channel']} (ROI: {bottom['ROI_pct']}%)")
print(f"\nFunnel:")
print(f"  Impressions → Clicks     : {funnel_vals[1]/funnel_vals[0]*100:.2f}% CTR")
print(f"  Clicks → Conversions     : {funnel_vals[2]/funnel_vals[1]*100:.2f}% Conv Rate")
print(f"\nBudget Recommendation:")
print(f"  Increase budget → Email, SEO")
print(f"  Reduce budget   → TV Ad (negative ROI: {bottom['ROI_pct']}%)")
