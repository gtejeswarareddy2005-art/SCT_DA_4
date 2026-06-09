# SCT_DA_4 — Business Insights Report (EDA)

**SkillCraft Technology | Data Analyst Internship | Task 04**

---

## 📌 Task Overview

Perform Exploratory Data Analysis (EDA) on a marketing campaign dataset. Focus on the "Why." Clean the data, visualize the funnel, and write a 1-page summary report recommending which marketing channels should receive more budget based on ROI.

---

## 🎯 Objectives

- Load and clean the marketing campaign dataset
- Engineer key metrics (ROI, CTR, Conversion Rate)
- Visualize the marketing funnel and channel performance
- Write a 1-page business insights report with budget recommendations

---

## 📂 Repository Structure

```
SCT_DA_4/
│
├── marketing_eda.py                        # Main EDA Python script
├── marketing_campaign.csv                  # Marketing campaign dataset
├── marketing_eda_dashboard.png             # EDA visualization dashboard
├── Marketing_Business_Insights_Report.docx # 1-page business summary report
└── README.md                               # Project documentation
```

---

## 🗂️ Dataset

**Marketing Campaign Dataset** — 1,000 campaigns across 6 channels and 4 regions.

| Property | Value |
|----------|-------|
| Rows | 1,000 |
| Columns | 10 |
| Channels | Email, SEO, Social Media, PPC, Influencer, TV Ad |
| Regions | North, South, East, West |
| Missing Values | 48 (handled during cleaning) |

**Columns:** Campaign_ID, Channel, Region, Age_Group, Month, Impressions, Clicks, Conversions, Cost, Revenue

---

## 🛠️ Tools & Libraries

| Tool | Purpose |
|------|---------|
| Python 3 | Programming language |
| Pandas | Data loading and cleaning |
| NumPy | Numerical computations |
| Matplotlib | Data visualization |

---

## 🧹 EDA Steps Performed

### 1. Data Cleaning
- Identified 48 missing values in Conversions and Revenue columns
- Filled missing values with median to preserve data integrity
- Zero missing values remain after cleaning

### 2. Feature Engineering
```python
df['ROI']                 = ((df['Revenue'] - df['Cost']) / df['Cost'] * 100)
df['CTR']                 = (df['Clicks'] / df['Impressions'] * 100)
df['Conv_Rate']           = (df['Conversions'] / df['Clicks'] * 100)
df['Cost_Per_Conversion'] = (df['Cost'] / df['Conversions'])
```

### 3. Visualizations (7 charts)
- ROI % by Marketing Channel
- Revenue Share by Channel (Pie chart)
- Cost vs Revenue scatter plot
- Conversions by Region
- Marketing Funnel
- Avg Click-Through Rate by Channel
- Monthly Revenue Trend

---

## 📊 Channel Performance Summary

| Channel | Total Cost | Total Revenue | ROI % | Recommendation |
|---------|-----------|---------------|-------|----------------|
| Email | $493,812 | $18,732,192 | 3,693% | ⬆ Increase Budget |
| SEO | $482,502 | $10,278,583 | 2,030% | ⬆ Increase Budget |
| Social Media | $507,939 | $5,257,783 | 935% | ↔ Maintain |
| PPC | $862,457 | $2,464,354 | 186% | ⬇ Optimize |
| Influencer | $778,976 | $2,018,919 | 159% | ⬇ Optimize |
| TV Ad | $787,214 | $263,267 | -67% | ⬇ Reduce Budget |

---

## 🔍 Marketing Funnel

| Stage | Count | Rate |
|-------|-------|------|
| Impressions | 13,477,032 | 100% |
| Clicks | 915,621 | 8.51% CTR |
| Conversions | 188,832 | 8.82% Conv Rate |

---

## 💡 Key Business Insights

- **Email** is the best performing channel with 3,693% ROI — increase budget by 30%
- **SEO** delivers strong sustainable returns at 2,030% ROI — increase budget by 20%
- **TV Ad** has a negative ROI of -67% — reduce budget by 60% immediately
- **Social Media** is performing well at 935% ROI — maintain current budget
- **PPC and Influencer** are underperforming relative to cost — optimize targeting before scaling
- **West region** leads in conversions; **South region** needs improvement

---

## ▶️ How to Run

1. Place `marketing_eda.py` and `marketing_campaign.csv` in the same folder
2. Run the script:
```bash
python marketing_eda.py
```
3. The dashboard `marketing_eda_dashboard.png` will be generated automatically

---

## 📚 Key Learnings

- EDA is about answering business questions, not just exploring data
- ROI-based analysis helps make data-driven budget decisions
- Funnel visualization reveals where customers drop off
- Not all expensive channels deliver value — TV Ad proved this clearly

---

*SkillCraft Technology — Data Analyst Internship*
