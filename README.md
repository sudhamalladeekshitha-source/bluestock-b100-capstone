# 🏦 Bluestock Fintech — Mutual Fund Analytics Capstone

## 📌 Project Overview
End-to-end mutual fund analytics pipeline covering 40 schemes across ETL, performance metrics, risk analytics, and Power BI dashboard development.

## 👤 Team
- Batch: 22A22J | Bluestock Fintech Internship | June 2026

## 📁 Project Structure
```
BlueFintech_internship/
├── 📓 Performance_Analytics.ipynb   # Task 4 - All 8 performance metrics
├── 📓 Advanced_Analytics.py         # Task 5 - VaR, Rolling Sharpe, HHI
├── 🐍 recommender.py               # Fund recommender by risk appetite
├── 🐍 run_pipeline.py              # Master execution script
├── 📊 bluestock_mf_dashboard.pbix  # Power BI Dashboard (4 pages)
├── 📄 Final_Report.pdf             # 15-20 page final report
├── 📑 Bluestock_MF_Presentation.pptx # 12-slide presentation
├── 📂 Datasets/
│   ├── nav_data.csv                # Daily NAV for 40 funds
│   ├── nifty50.csv                 # Nifty 50 benchmark
│   ├── nifty100.csv                # Nifty 100 benchmark
│   ├── expense_ratio.csv           # Fund expense ratios
│   ├── fund_scorecard.csv          # Composite scores 0-100
│   ├── alpha_beta.csv              # OLS regression results
│   ├── var_cvar_report.csv         # VaR & CVaR analysis
│   └── investor_data.csv           # Investor transaction data
└── 📂 Charts/
    ├── benchmark_comparison_chart.png
    └── rolling_sharpe_chart.png
```

## ⚙️ Setup Instructions

### 1. Install Requirements
```bash
pip install pandas numpy matplotlib seaborn scipy python-pptx reportlab
```

### 2. Clone Repository
```bash
git clone <your-repo-url>
cd BlueFintech_internship
```

### 3. Run Full Pipeline
```bash
python run_pipeline.py
```

## 📊 How to Run Individual Tasks

### Task 4 - Fund Performance Analytics
```bash
# Open in Jupyter or VS Code
Performance_Analytics.ipynb
```

### Task 5 - Advanced Analytics
```bash
python Advanced_Analytics.py
```

### Fund Recommender
```bash
python recommender.py
# Enter: Low / Moderate / High
```

## 📈 How to Open the Dashboard
1. Install **Power BI Desktop** from microsoft.com
2. Open `bluestock_mf_dashboard.pbix`
3. Navigate 4 pages: Industry Overview → Fund Performance → Investor Analytics → SIP Trends

## 📋 Dataset Descriptions
| File | Rows | Description |
|------|------|-------------|
| nav_data.csv | 1,566 | Daily NAV for 40 funds (2019-2024) |
| nifty50.csv | 1,566 | Nifty 50 index daily close |
| nifty100.csv | 1,566 | Nifty 100 index daily close |
| fund_scorecard.csv | 40 | Composite scores (0-100) |
| alpha_beta.csv | 40 | OLS regression vs Nifty 100 |
| var_cvar_report.csv | 40 | Value at Risk (95%) & CVaR |
| investor_data.csv | 1,270 | SIP/Lumpsum transaction records |

## 🏆 Key Results
- **Top Fund**: Tata Large Cap (Score: 88.88/100, CAGR: 85.28%)
- **Best Sharpe**: Canara Robeco Bluechip (1.50)
- **Highest Risk**: Nippon India Small Cap (VaR: -2.16%)
- **At-Risk Investors**: 53 of 88 (60%) with SIP gap >35 days

## 📦 Deliverables
- ✅ Performance_Analytics.ipynb
- ✅ Advanced_Analytics.py + recommender.py
- ✅ bluestock_mf_dashboard.pbix
- ✅ fund_scorecard.csv
- ✅ alpha_beta.csv
- ✅ var_cvar_report.csv
- ✅ Bluestock_MF_Presentation.pptx
- ✅ Final_Report.pdf
